import kivy
kivy.require('1.10.1')
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg, NavigationToolbar2Kivy, FigureCanvas
import matplotlib.pyplot as plt; plt.rcdefaults()
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
import socket
import pickle
import struct  ## new
import cv2
from Methods import Sensors,TheGuage
import numpy as np
import random
import datetime
from matplotlib.dates import DateFormatter
import pandas as pd
import matplotlib.style as style
import mqttDemoScripts.guiSubscriber as guiSub
import mqttDemoScripts.controlPublisher as controlPub

style.use('seaborn-poster')
style.use('ggplot')
matplotlib.rcParams['font.family'] = "serif"

Builder.load_file("app.kv")

class KivyCamera(Image):

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.connectionFail = Popup(title='Connection Error', content=Label(text='There was an issue connecting to the camera.'), size_hint=(.4,.4),auto_dismiss=True)
        self.connectionDropped = Popup(title='Connection Dropped', content=Label(text='The connection to the robot was dropped. Try reconnecting'),size_hint=(.4, .4), auto_dismiss=True)

    def start(self, fps=60):
        HOST = ''
        PORT = 8485

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(5)
        print('Socket created')
        self.s.bind((HOST, PORT))
        print('Socket bind complete')
        try:
            self.s.listen(1)
            print('Socket now listening')
            self.conn, self.addr = self.s.accept()
            self.data = b""
            self.payload_size = struct.calcsize(">L")
            print('connected')
            print("payload_size: {}".format(self.payload_size))
            Clock.schedule_interval(self.update, 1.0/fps)
        except:
            self.connectionFail.open()
            print("connection failed")

    def update(self, dt):
        print("update")
        try:
            while len(self.data) < self.payload_size:
                print("Recv: {}".format(len(self.data)))
                self.data += self.conn.recv(4096)
            print("Done Recv: {}".format(len(self.data)))
            packed_msg_size = self.data[:self.payload_size]
            self.data = self.data[self.payload_size:]
            self.msg_size = struct.unpack(">L", packed_msg_size)[0]
            print("msg_size: {}".format(self.msg_size))

            while len(self.data) < self.msg_size:
                self.data += self.conn.recv(4096)

            self.frame_data = self.data[:self.msg_size]
            print(self.frame_data)
            self.data = self.data[self.msg_size:]
            self.frame = pickle.loads(self.frame_data, fix_imports=True, encoding="bytes")
            self.frame = cv2.imdecode(self.frame, cv2.IMREAD_COLOR)
            self.frame = cv2.flip(self.frame,0)
            texture = self.texture
            w, h = self.frame.shape[1], self.frame.shape[0]
            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
            texture.blit_buffer(self.frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()
        except:
            Clock.unschedule(self.update)
            self.connectionDropped.open()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.loginFail = Popup(title='Login Fail', content=Label(text='user: username\npass: password'), size_hint=(.4,.4),auto_dismiss=True)
        self.initController()
        Clock.schedule_interval(self.Xboxcontroller,1/5)

    def verify_credentials(self):
        if self.ids["login"].text == "username" and self.ids["passw"].text == "password":
            self.manager.switch_to(MainScreen(name='main'))
            Window.size = (900,600)
        else:
            self.loginFail.open()
    def initController(self,broker='127.0.0.1', port=1883, topic='controllerTest'):
        tracker = 0
        sensorData = ''
        #broker is me
        self.cliePub = controlPub.controlPublisher()

        self.cliePub.buildPublisher()
        self.cliePub.addPublisherParams(broker, port, topic)

        self.cliePub.connectPublisher()

        d = self.cliePub.checkConnection()
        c = self.cliePub.checkClientDetails()

        print("Publisher details")
        print(c)
        print("Publisher is connected: ")
        print(d)
        pubClient = self.cliePub.getClient()
        print(pubClient)
        print('Here in the publisher')
        self.cliePub.initController()
        self.cliePub.actionTypeCreator()

    def Xboxcontroller(self,dt):
        mvmntData = self.cliePub.actionIdentifier()

        print('Sending mvmnt data to the subscriber')
        print('\n')
        print(mvmntData)
        #time.sleep(1)
        status = self.cliePub.publishMvmnt(mvmntData)
        print('Data published')

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Window.size = (900,600)

        self.Gg = TheGuage()
        self.gFig,self.gAx,self.gArrow = self.Gg.gauge(title='Air Quality', colors='Reds_r')
        self.canvas3 = self.gFig.canvas
        self.ids.guage1.add_widget(self.canvas3)


        self.index = ["Ambient Temperature"]
        temp = [11]
        self.temperature = pd.DataFrame({'Ambient Temperature': temp}, index=self.index)
        self.fig4, self.ax4 = plt.subplots()
        self.fig4.patch.set_alpha(0.0)

        self.ax4.tick_params(axis='x', colors='white')
        self.ax4.tick_params(axis='y', colors='white')
        self.bar = self.fig4.canvas
        self.temperature.plot(ax=self.ax4, kind='bar', color='black', legend=False, title='Ambient Temperature', rot=0, ylim=(0,100))
        self.ids.temperature.add_widget(self.bar)
        self.celcius = True

        mqttCon,mqttdetails = self.initializeMqtt()
        if mqttCon == 1:
            self.connectionStatus = Popup(title='Connection Status', content=Label(text='Data connection successful'),size_hint=(.4,.4),auto_dismiss=(True))
        elif mqttCon == 0:
            self.connectionStatus = Popup(title='Connection Status', content=Label(text='Data connection not successful'))

        self.connectionStatus.open()

        Clock.schedule_interval(self.updateData,1)

        Clock.schedule_interval(self.updateTemp,1)
        self.graphit()
        Clock.schedule_interval(self.updateGuage,1/15)

        self.fullscreen = False
        self.freeze = False

    def initializeMqtt(self,broker='143.215.95.16', port=1883, topic='guiParseTest'):
        self.clieSub = guiSub.guiSubscriber()
        self.clieSub.buildSubscriber()
        self.clieSub.addSubscriberParams(broker, port, topic)
        self.clieSub.connectSubscriber()
        a = self.clieSub.checkConnection()
        b = self.clieSub.checkClientDetails()
        # print("Subscriber details")
        print(b)
        # print("Subscriber is connected: ")
        print(a)
        subClient = self.clieSub.getClient()
        print(subClient)
        print('Here in the subscriber')
        return a, b

    def updateData(self,dt):
        print('Data received')
        sensorData = self.clieSub.receiveGuiData()
        print('Output from receive Gui Data')
        print(sensorData)
        # tracker += 1
        # print('At ' + str(tracker) + ' second ' + str(status))
        self.Data = self.clieSub.parseGuiData(sensorData)
        print('Data parsed into dictionary')
        print(self.Data)
        print('\n')

    def updateTemp(self,dt):
        self.ax4.clear()
        tempC = self.Data.get('AmbientTempSensor')
        print(tempC)
        if self.celcius:
            self.temp = tempC
            ymax = 100
        else:
            self.temp = 9.0 / 5.0 * tempC + 32
            ymax = 215

        if self.temp <= 25:
            color = 'blue'
        elif self.temp > 25 and self.temp <= 50:
            color = 'yellow'
        elif self.temp > 50 and self.temp <= 75:
            color = 'orange'
        else:
            color = 'red'
        self.temperature = pd.DataFrame({'Ambient Temperature': self.temp}, index=self.index)
        self.temperature.plot(ax=self.ax4, kind='bar', color=color, legend=False, title='Ambient Temperature', rot=0, ylim=(0,ymax))
        self.fig4.canvas.draw()
        self.ids.Templabel.text = str(self.temp)+u'\N{DEGREE SIGN}'+"C"

    def updateGuage(self,dt):
        self.gArrow.remove()
        airQuality = self.Data.get('AirQualitySensor')
        pos = 180 - abs(10-airQuality)*10
        if pos > 180:
            pos = 180
        elif pos < 0:
            pos = 0

        self.gArrow = self.gAx.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), \
                       width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')
        self.gFig.canvas.draw()

    def press(self,event):
        print('press released from test', event.x, event.y, event.button)

    def release(self,event):
        print('release released from test', event.x, event.y, event.button)

    def keypress(self,event):
        print('key down', event.key)

    def keyup(self,event):
        print('key up', event.key)
        if str(event.key) == 'f' and self.freeze == False:
            self.freeze = True
        elif str(event.key) == 'f' and self.freeze == True:
            self.freeze = False
        elif str(event.key) == 't':
            self.manager.current = 'graphs'

    def motionnotify(self,event):
        print('mouse move to ', event.x, event.y)

    def resize(self,event):
        print('resize from mpl ', event.width, event.height)

    def scroll(self,event):
        print('scroll event from mpl ', event.x, event.y, event.step)

    def figure_enter(self,event):
        print('figure enter mpl')

    def figure_leave(self,event):
        print('figure leaving mpl')

    def close(self,event):
        print('closing figure')

    def graphit(self):
        self.fig, (self.ax,self.ax2) = plt.subplots(nrows=2,sharex=True)
        self.ax2.set_xlabel('common xlabel')
        self.ax2.set_ylabel('common ylabel')
        self.sensors = Sensors()

        self.fig.canvas.mpl_connect('button_press_event', self.press)
        self.fig.canvas.mpl_connect('button_release_event', self.release)
        self.fig.canvas.mpl_connect('key_press_event', self.keypress)
        self.fig.canvas.mpl_connect('key_release_event', self.keyup)
        self.fig.canvas.mpl_connect('resize_event', self.resize)
        self.fig.canvas.mpl_connect('scroll_event', self.scroll)
        self.fig.canvas.mpl_connect('close_event', self.close)

        canvas = self.fig.canvas
        self.liveGraph = BoxLayout(orientation="vertical")
        nav1 = NavigationToolbar2Kivy(canvas)
        self.liveGraph.add_widget(nav1.actionbar)
        self.liveGraph.add_widget(canvas)
        self.ids.graph.add_widget(self.liveGraph)
        self.ax2.set_ylabel('common ylabel')

        self.graphData = pd.DataFrame(columns=('time','audio','temperature'))
        Clock.schedule_interval(self.refreshGraphData,1)

    def refreshGraphData(self,dt):
        self.ax.set_ylabel('hesfidoj')
        self.ax2.set_ylabel('common ylabel')
        y = self.Data.get('ObjectTempSensor')
        y2 = random.randint(1, 70)
        newdata = [datetime.datetime.now(), y, y2]
        self.graphData.loc[-1] = newdata  # adding a row
        self.graphData.index = self.graphData.index + 1  # shifting index
        self.graphData = self.graphData.sort_index()  # sorting by index
        self.graphData.append(newdata, ignore_index=False)
        self.graphData.reset_index()
        self.graphData['time'] = pd.to_datetime(self.graphData['time'], unit='s')
        self.graphData = self.graphData.head(800)
        if self.fullscreen == False and self.freeze == False:
            graph = self.graphData.head(300)
            self.ax.clear()
            self.ax2.clear()
            graph.plot(x='time', y='audio', ax=self.ax, kind='line', color='black', legend=False)
            graph.plot(x='time', y='temperature', ax=self.ax2, kind='line', color='black', legend=False)
            ## Rotate date labels automatically
            self.fig.autofmt_xdate()
            self.fig.canvas.draw()
            myFmt = DateFormatter('%H:%M:%S')
            self.ax.xaxis.set_major_formatter(myFmt)
        else:
            pass

    def changesize(self):
        if self.fullscreen:
            self.ids.cambox.size_hint = (.5,.5)
            self.ids.fullscreen.text = "Fullscreen"
            self.ids.graph.add_widget(self.liveGraph)
            self.fullscreen = False
        else:
            self.ids.cambox.size_hint = (1,1)
            self.ids.fullscreen.text = "Minimize"
            self.ids.graph.remove_widget(self.liveGraph)
            self.fullscreen = True

    def dostart(self, *largs):
        self.ids.qrcam.start()

class Options(Screen):
    def __init__(self, **kwargs):
        super(Options, self).__init__(**kwargs)
        pass

class Graphs(Screen):
    def __init__(self,**kwargs):
        super(Graphs,self).__init__(**kwargs)

        self.graph = BoxLayout(orientation="vertical")
        self.fig, (self.ax,self.ax2) = plt.subplots(nrows=2,sharex=True)
        self.ids.graph.add_widget(self.graph)
        canvas = self.fig.canvas
        nav1 = NavigationToolbar2Kivy(canvas)
        self.graph.add_widget(nav1.actionbar)
        self.graph.add_widget(canvas)
        self.fig.canvas.mpl_connect('key_press_event', self.keypress)

    def on_enter(self, *args):
        self.manager.get_screen('main').onMain=False

    def keypress(self,event):
        print('key press', event.key)
        if str(event.key) == 't':
            self.manager.current = 'main'

    def redrawGraph(self):
        graph = self.manager.get_screen('main').graphData.head(1000)
        self.ax.clear()
        self.ax2.clear()
        graph.plot(x='time', y='audio', ax=self.ax, kind='line', color='black', legend=False)
        graph.plot(x='time', y='temperature', ax=self.ax2, kind='line', color='black', legend=False)
        self.fig.autofmt_xdate()
        self.fig.canvas.draw()
        myFmt = DateFormatter('%H:%M:%S')
        self.ax.xaxis.set_major_formatter(myFmt)



sm = ScreenManager(transition=SwapTransition())
sm.add_widget(LoginScreen(name='login'))
#sm.add_widget(MainScreen(name='main'))
#sm.add_widget(Options(name='options'))
#sm.add_widget(Graphs(name='graphs'))


class MyApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MyApp().run()


