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
from kivy.uix.camera import Camera
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import cv2
import random

from kivy.properties import StringProperty

Builder.load_file("myapp.kv")

class KivyCamera(Image):

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = None

    def start(self, capture, fps=60):
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        Clock.unschedule_interval(self.update)
        self.capture = None

    def update(self, dt):
        return_value, frame = self.capture.read()
        if return_value:
            texture = self.texture
            w, h = frame.shape[1], frame.shape[0]
            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()


class LoginScreen(Screen):
    def verify_credentials(self):
        if self.ids["login"].text == "username" and self.ids["passw"].text == "password":
            self.manager.current = "main"
            #Window.fullscreen = 'auto'
        else:
            pass
    Window.fullscreen = False
    Window.size = (300,300)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.change_text, 1)

    def init_qrtest(self):
        pass

    def dostart(self, *largs):
        global capture
        capture = cv2.VideoCapture(cv2.CAP_DSHOW)
        self.ids.qrcam.start(capture)

    def doexit(self):
        global capture
        if capture != None:
            capture.release()
            capture = None
        EventLoop.close()

    def startit(self):
        Clock.schedule_interval(self.change_text, 1)

    def change_text(self, *args):
        self.lbl1.text = str(random.randint(1,100))
        self.lbl2.text = str(random.randint(1,100))
        self.lbl3.text = str(random.randint(1,100))



#class OptionsScreen(GridLayout, Screen):
#    pass

sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(MainScreen(name='main'))

dropdown = DropDown()
for index in range(5):
    btn = Button(text='value %d' % index, size_hint_y=None, height=44)
    btn.bind(on_release=lambda btn:dropdown.select(btn.text))
    dropdown.add_widget(btn)

mainbutton = Button(text='Hello', size_hint=(None,None))
mainbutton.bind(on_release=dropdown.open)
dropdown.bind(on_select=lambda instance, x: setattr(mainbutton,'text',x))



class MyApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MyApp().run()


