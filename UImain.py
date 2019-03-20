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
import matplotlib.pyplot as plt
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import socket
import pickle
import struct  ## new
import cv2
from Methods import Sensors
from kivy.graphics import Color, Line, Rectangle
import numpy as np
from matplotlib.patches import Circle, Wedge, Rectangle
from matplotlib import cm
import random
import datetime
from matplotlib.dates import DateFormatter
import pandas as pd
import matplotlib.style as style
style.use('seaborn-poster')
style.use('ggplot')
matplotlib.rcParams['font.family'] = "serif"

Builder.load_file("app.kv")

class TheGuage():
    def __init__(self):
        pass

    def degree_range(self,n):
        start = np.linspace(0, 180, n+1, endpoint=True)[0:-1]
        end = np.linspace(0, 180, n+1, endpoint=True)[1::]
        mid_points = start + ((end-start)/2.)
        return np.c_[start, end], mid_points

    def rot_text(self,ang):
        rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
        return rotation


    def gauge(self,labels=['LOW', 'MEDIUM', 'HIGH', 'VERY HIGH', 'EXTREME'], colors='jet_r', arrow=1, title='', fname=False):
        """
        some sanity checks first
        """

        N = len(labels)
        if arrow > N:
            raise Exception("\n\nThe category ({}) is greated than \
            the length\nof the labels ({})".format(arrow, N))

        """
        if colors is a string, we assume it's a matplotlib colormap
        and we discretize in N discrete colors 
        """

        if isinstance(colors, str):
            cmap = cm.get_cmap(colors, N)
            cmap = cmap(np.arange(N))
            colors = cmap[::-1, :].tolist()
        if isinstance(colors, list):
            if len(colors) == N:
                colors = colors[::-1]
            else:
                raise Exception("\n\nnumber of colors {} not equal \
                to number of categories{}\n".format(len(colors), N))

        """
        begins the plotting
        """

        fig3, ax3 = plt.subplots()
        canvas3 = fig3.canvas
        ang_range, mid_points = self.degree_range(N)
        print(ang_range)

        labels = labels[::-1]

        """
        plots the sectors and the arcs
        """
        patches = []
        for ang, c in zip(ang_range, colors):
            # sectors
            patches.append(Wedge((0., 0.), .4, *ang, facecolor='w', lw=2))
            # arcs
            patches.append(Wedge((0., 0.), .4, *ang, width=0.10, facecolor=c, lw=2, alpha=0.5))

        [ax3.add_patch(p) for p in patches]

        """
        set the labels (e.g. 'LOW','MEDIUM',...)
        """

        for mid, lab in zip(mid_points, labels):
            ax3.text(0.35 * np.cos(np.radians(mid)), 0.35 * np.sin(np.radians(mid)), lab, horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight='bold', rotation=self.rot_text(mid))

        """
        set the bottom banner and the title
        """
        r = Rectangle((-0.4, -0.1), 0.8, 0.1, facecolor='w', lw=2)
        ax3.add_patch(r)

        ax3.text(0, -0.05, title, horizontalalignment='center', verticalalignment='center', fontsize=22, fontweight='bold')

        """
        plots the arrow now
        """

        pos = mid_points[abs(arrow - N)]

        ax3.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')

        ax3.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
        ax3.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))

        """
        removes frame and ticks, and makes axis equal and tight
        """

        ax3.set_frame_on(False)
        ax3.axes.set_xticks([])
        ax3.axes.set_yticks([])
        ax3.axis('equal')
        plt.tight_layout()

        if fname:
            fig3.savefig(fname, dpi=200)

        return canvas3

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
            self.s.listen(2)
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

    def verify_credentials(self):
        if self.ids["login"].text == "username" and self.ids["passw"].text == "password":
            self.manager.current = "main"
            Window.size = (900,600)
        else:
            self.loginFail.open()
    Window.fullscreen = False
    Window.size = (300,300)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Window.size = (900,600)
        Gg = TheGuage()
        g = Gg.gauge(labels=['LOW','MEDIUM','HIGH','VERY HIGH','EXTREME','CRITICAL'],colors='YlOrRd_r', arrow=1, title='Air Quality')
        self.ids.guage1.add_widget(g)
        self.graphit()
        self.fullscreen = False
        self.freeze = False

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
        self.sensors = Sensors()

        self.fig.canvas.mpl_connect('button_press_event', self.press)
        self.fig.canvas.mpl_connect('button_release_event', self.release)
        self.fig.canvas.mpl_connect('key_press_event', self.keypress)
        self.fig.canvas.mpl_connect('key_release_event', self.keyup)
        self.fig.canvas.mpl_connect('resize_event', self.resize)
        self.fig.canvas.mpl_connect('scroll_event', self.scroll)
        self.fig.canvas.mpl_connect('close_event', self.close)

        canvas = self.fig.canvas
        self.a = BoxLayout(orientation="vertical")
        nav1 = NavigationToolbar2Kivy(canvas)
        self.a.add_widget(nav1.actionbar)
        self.a.add_widget(canvas)
        self.ids.graph.add_widget(self.a)

        self.graphData = pd.DataFrame(columns=('time','audio','temperature'))

        Clock.schedule_interval(self.refreshGraphData,1/800)

    def refreshGraphData(self,dt):
        if self.fullscreen == False:
            #self.ids.graph.remove_widget(self.a)
            print("Refreshing data...")
            y = random.randint(1, 50)
            y2 = random.randint(1,70)
            newdata = [datetime.datetime.now(), y, y2]
            self.graphData.loc[-1] = newdata  # adding a row
            self.graphData.index = self.graphData.index + 1  # shifting index
            self.graphData = self.graphData.sort_index()  # sorting by index
            self.graphData.append(newdata, ignore_index=False)
            self.graphData.reset_index()
            self.graphData['time'] = pd.to_datetime(self.graphData['time'], unit='s')
            self.graphData = self.graphData.head(1000)

            #ax.clear()
            if self.freeze == False:
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
            #self.ids.graph.add_widget(self.a)

    def changesize(self):
        print('this')
        if self.fullscreen:
            self.ids.cambox.size_hint = (.5,.5)
            self.ids.fullscreen.text = "Fullscreen"
            self.ids.graph.add_widget(self.a)
            self.fullscreen = False
        else:
            self.ids.cambox.size_hint = (1,1)
            self.ids.fullscreen.text = "Minimize"
            self.ids.graph.remove_widget(self.a)
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

        self.a = BoxLayout(orientation="vertical")
        self.fig, (self.ax,self.ax2) = plt.subplots(nrows=2,sharex=True)
        self.ids.graph.add_widget(self.a)
        canvas = self.fig.canvas
        nav1 = NavigationToolbar2Kivy(canvas)
        self.a.add_widget(nav1.actionbar)
        self.a.add_widget(canvas)
        self.fig.canvas.mpl_connect('key_press_event', self.keypress)

    def keypress(self,event):
        print('key press', event.key)
        if str(event.key) == 't':
            self.manager.current = 'main'

    def thing(self):
        graph = self.manager.get_screen('main').graphData.head(1000)
        print(graph)
        self.ax.clear()
        self.ax2.clear()
        graph.plot(x='time', y='audio', ax=self.ax, kind='line', color='black', legend=False)
        graph.plot(x='time', y='temperature', ax=self.ax2, kind='line', color='black', legend=False)
        self.fig.autofmt_xdate()
        self.fig.canvas.draw()
        myFmt = DateFormatter('%H:%M:%S')
        self.ax.xaxis.set_major_formatter(myFmt)



sm = ScreenManager()
#sm.add_widget(LoginScreen(name='login'))
sm.add_widget(MainScreen(name='main'))
#sm.add_widget(Options(name='options'))
sm.add_widget(Graphs(name='graphs'))


class MyApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MyApp().run()


