import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.base import runTouchApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown

class LoginScreen(GridLayout):

    def __init__(self,**kwargs):
        super(LoginScreen,self).__init__(**kwargs)
        LoginScreen.cols = 2
        LoginScreen.spacing = [100,100]
        self.add_widget(Label(text='User Name',size_hint=(.05,.1)))
        self.username = TextInput(multiline=False, size_hint=(.05,.1))
        self.add_widget(self.username)
        self.add_widget(Label(text='password',size_hint=(.05,.1)))
        self.password = TextInput(password=True, multiline=False,size_hint=(.05,.1))
        self.add_widget(self.password)
        self.button = Button(size_hint=(.05,.005), text="hello")
        self.add_widget(self.button)
        self.add_widget(mainbutton)

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
        return LoginScreen()

if __name__ == '__main__':
    MyApp().run()


