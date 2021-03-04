#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 14:49:19 2020

@author: bhaskar
"""

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton




#
#CameraControl = BoxLayout(orientation='vertical')
#CameraControl.add_widget(Label('Camera Control'))
#previewButton = ToggleButton(text='Camera Preview')
#CameraControl.add_widget(previewButton)
#
#
#
#VisLEDControl = BoxLayout(orientation='vertical')
#VisLEDControl.add_widget(Label('White LED Control'))
#vislight1 = ToggleButton(text='Set 1')
#VisLEDControl.add_widget(vislight1)
#vislight2 = ToggleButton(text='Set 2')
#VisLEDControl.add_widget(vislight2)
#vislight3 = ToggleButton(text='Set 3')
#VisLEDControl.add_widget(vislight3)
#vislight4 = ToggleButton(text='Set 4')
#VisLEDControl.add_widget(vislight4)
#vislight5 = ToggleButton(text='Set 5')
#VisLEDControl.add_widget(vislight5)
#vislight6 = ToggleButton(text='Set 6')
#VisLEDControl.add_widget(vislight6)
#  

        
        

#VisLEDControl = BoxLayout(orientation='vertical')


#
#class MainWindow(BoxLayout):
#    def __init__(self, **kwargs):
#        super(MainWindow, self).__init__(**kwargs)
#        MainWindow.layout = BoxLayout(orientation='vertical') #consists of two subparts: title, and control panel (boxlayout horiz)
#        MainWindow.add_widget(Label("Mosquito Video Chamber - Control Panel"))

#

class VisLightControl(Screen):
#    def __init__(self, **kwargs):
#        super(VisLightControl, self).__init__(**kwargs)
        layout = BoxLayout(orientation ='vertical')
        top_buttons=BoxLayout()
        layout.add_widget(top_buttons) # <--------
        top_buttons.add_widget(save=Button(text='Save')
        
#        self.add_widget(testLayout)
#        
#        self.add_widget(Label(text='White LED Control'))
#        vislight1 = ToggleButton(text='Set 1')
#        self.add_widget(vislight1)
#        vislight2 = ToggleButton(text='Set 2')
#        self.add_widget(vislight2)
#        vislight3 = ToggleButton(text='Set 3')
#        self.add_widget(vislight3)
#        vislight4 = ToggleButton(text='Set 4')
#        self.add_widget(vislight4)
#        vislight5 = ToggleButton(text='Set 5')
#        self.add_widget(vislight5)
#        vislight6 = ToggleButton(text='Set 6')
#        self.add_widget(vislight6)
#  
#
#      
#
#class IrLightControl(GridLayout):
#    def __init__(self, **kwargs):
#        super(IrLightControl, self).__init__(**kwargs)
#        self.cols = 1
#        self.add_widget(Label(text='IR LED Control'))
#        irlight1 = ToggleButton(text='Set 1')
#        self.add_widget(irlight1)
#        irlight2 = ToggleButton(text='Set 2')
#        self.add_widget(irlight2)
#        irlight3 = ToggleButton(text='Set 3')
#        self.add_widget(irlight3)
#        irlight4 = ToggleButton(text='Set 4')
#        self.add_widget(irlight4)
#        irlight5 = ToggleButton(text='Set 5')
#        self.add_widget(irlight5)
#        irlight6 = ToggleButton(text='Set 6')
#        self.add_widget(irlight6)
#        
##
#class ControlPanel(BoxLayout):
#    def __init__(self, **kwargs):
#        super(LightControl, self).__init__(**kwargs)
#        self.cols = 2
#        self.rows = 7
#        self.add_widget(Label(text='White LED Control'))
#        vislight1 = ToggleButton(text='Set 1')
#        self.add_widget(vislight1)
#        vislight2 = ToggleButton(text='Set 2')
#        self.add_widget(vislight2)
#        vislight3 = ToggleButton(text='Set 3')
#        self.add_widget(vislight3)
#        vislight4 = ToggleButton(text='Set 4')
#        self.add_widget(vislight4)
#        vislight5 = ToggleButton(text='Set 5')
#        self.add_widget(vislight5)
#        vislight6 = ToggleButton(text='Set 6')
#        self.add_widget(vislight6)
#        
#        self.add_widget(Label(text='IR LED Control'))
#        irlight1 = ToggleButton(text='Set 1')
#        self.add_widget(irlight1)
#        irlight2 = ToggleButton(text='Set 2')
#        self.add_widget(irlight2)
#        irlight3 = ToggleButton(text='Set 3')
#        self.add_widget(irlight3)
#        irlight4 = ToggleButton(text='Set 4')
#        self.add_widget(irlight4)
#        irlight5 = ToggleButton(text='Set 5')
#        self.add_widget(irlight5)
#        irlight6 = ToggleButton(text='Set 6')
#        self.add_widget(irlight6)
#        
    

        
class MyApp(App):
    def build(self):
        return VisLightControl()
    
if __name__ == '__main__':
    MyApp().run()
    
