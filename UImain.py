import kivy
kivy.require('1.10.1')
from kivy.lang import Builder
from kivy.app import App
from kivy.base import EventLoop
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import socket
import pickle
import struct  ## new
import cv2
import random
from Methods import Sensors

Builder.load_file("app.kv")

class KivyCamera(Image):

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.connectionFail = Popup(title='Connection Error', content=Label(text='There was an issue connecting to the camera.'), size_hint=(.4,.4),auto_dismiss=True)

    def start(self, fps=60):
        HOST = ''
        PORT = 8485

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(.5)
        print('Socket created')
        s.bind((HOST, PORT))
        print('Socket bind complete')
        try:
            s.listen(2)
            print('Socket now listening')
            self.conn, self.addr = s.accept()
            self.data = b""
            self.payload_size = struct.calcsize(">L")
            print("payload_size: {}".format(self.payload_size))
            Clock.schedule_interval(self.update, 1.0/fps)
        except:
            self.connectionFail.open()
            print("connection failed")

    def stop(self):
        Clock.unschedule_interval(self.update)
        self.capture = None

    def update(self, dt):
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


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.navigationdrawer = NavigationDrawer()
        side_panel = BoxLayout(orientation='vertical')
        side_panel.add_widget(Label(text='Panel label'))
        buttonthing = Button(text='press me to change the thing')

        def change(instance):
            self.manager.current = "main"

        buttonthing.bind(on_press=change)
        side_panel.add_widget(buttonthing)
        side_panel.add_widget(Button(text='Another button'))
        self.navigationdrawer.add_widget(side_panel)

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
        Clock.schedule_interval(self.change_text, 1/5)

    def init_qrtest(self):
        pass

    def dostart(self, *largs):
        self.ids.qrcam.start()


    def logoff(self):
        if self.capture != None:
            self.capture.release()
        EventLoop.close()

    def change_text(self, *args):
        self.lbl1.text = str(random.randint(1,100))
        self.lbl2.text = str(random.randint(1,100))
        self.lbl3.text = str(random.randint(1,100))

class Graphs(Screen):
    def __init__(self, **kwargs):
        super(Graphs, self).__init__(**kwargs)

sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(MainScreen(name='main'))
sm.add_widget(Graphs(name='graphs'))


class MyApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MyApp().run()


