from kivy.app import App
from kivy.lang import Builder
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton


Builder.load_string('''

<ToggleButton>:
    on_state: app.root.on_state(self)

<MainScreen>:

    BoxLayout:

        ToggleButtons:



''')

class MainScreen(BoxLayout):

    def on_state(self, togglebutton):
        tb = togglebutton
        print(tb,tb.state,tb.text)


class ToggleButtons(StackLayout):
    lista = ["aloes", "blonnik", "herbata biala", "herbata czerwona", "herbata zielona", "mleko kokosowe", "mleko migdalowe", "mleko owsiane", "mleko ryzowe", "mleko sojowe", "woda kokosowa"]

    def __init__(self,**kwargs):
        super(ToggleButtons,self).__init__(**kwargs)
        for i in self.lista:
            tgbtn = ToggleButton(text = i,size_hint = (.1, .30))

            self.add_widget(tgbtn)


class MyApp(App):
     def build(self):
        return MainScreen()


MyApp().run()