#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 13:25:26 2020

@author: Bhaskar Yechuri

Purpose: Python application to be run on a raspberry pi connected to a camera, allowing for automated and standardized recordings of mosquito behavioral assays.
"""
#for gpio & other general functionality
import sys
import os
from gpiozero import LED
from time import sleep
from time import strftime
from time import localtime
from time import time
import psutil

#for camera functionality
from picamera import PiCamera
from time import sleep
from time import strftime

#for kivy/UI functionality
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout

#pins that can be used to turn on/off LED sets connected to the Rpi
led1 = LED(3)
led2 = LED(27)
led3 = LED(10)

#initialize camera objects and set global variables/camera defaults
camera = PiCamera()
brightness = 50
ISO = 0
contrast = 0
exp_comp = 0
saturation = 0
sharpness = 0
folder = "/home/pi/Desktop/" #default location to save videos & images

#kivy application starts here, and reads from test.kv file to create UI & its functionality
#this section all the functions that are called when buttons in the UI are pressed 
class ContainerFloat(FloatLayout):    
    def __init__(self, **kwargs):
        super(ContainerFloat, self).__init__(**kwargs)
        global camera
        if(camera.closed):
            camera = PiCamera() #the moment the app is launched, the camera object is initalized
    
    #simple functions to turn on/off the LEDs
    def LED1_on(self):
        led1.on()
    def LED2_on(self):
        led2.on()
    def LED3_on(self):
        led3.on()
        
    def LED1_off(self):
        led1.off()
    def LED2_off(self):
        led2.off()
    def LED3_off(self):
        led3.off()

    #opens preview when preview button is clicked. Closes existing preview window (if it exists) and opens a new one
    def preview_on(self):
        global camera #global keyword tells it that the camera variable to be used is the global one
        if(camera.closed):
            camera = PiCamera()
        
        if(camera.preview == None):
            print("turning preview on")
            camera.start_preview(fullscreen=False, window = (400, 100, 400, 200))
            sleep(2)
        else:
            print("preview window active, will close and reopen")
            camera.stop_preview()
            camera.start_preview(fullscreen=False, window = (400, 100, 400, 200))
            sleep(2)
    
    def preview_off(self):
        global camera
        if(camera.closed):
            camera = PiCamera()
        print("turning preview off")
        camera.stop_preview()
    
    #initiates manual recording. This function is called on both ends of the manual recording (to start and stop it)
    def record_toggle(self,path):
        #use global keyword to tell it to use the global variables instead of creating new local ones
        global camera
        global camera
        global brightness
        global ISO
        global contrast
        global exp_comp
        global saturation
        global sharpness
        
        if(camera.closed):
            camera = PiCamera()
            
        if camera.recording == True:
            print("stopping the recording")
            camera.stop_recording()
            camera.stop_preview()
            sleep(2)
        else:
            print("starting to record")
            full_datetime = strftime("%d_%m_%y_at_%I_%M%p")
            filename = 'ManualVideo_on_'+ full_datetime + ".h264"
            
            camera.brightness = brightness
            camera.iso = ISO
            camera.contrast = contrast
            camera.exposure_compensation = exp_comp
            camera.saturation = saturation
            camera.sharpness = sharpness
            
            camera.framerate = 30
            
            camera.start_preview(fullscreen=False, window = (400, 100, 400, 200))
            print("filename is", path  + "/"+ filename)
            camera.start_recording(path  + "/"+ filename)
            sleep(2)
        return
    
    #function to start a timed recording. Currently, there is no software-defined way to end a timed recording except waiting for the end or closing the program    
    def timed_record_on(self,mins_to_record,path):
        global camera
        global brightness
        global ISO
        global contrast
        global exp_comp
        global saturation
        global sharpness
        
        if(camera.closed):
            camera = PiCamera()
            
        mins_to_record = float(mins_to_record)
        full_datetime = strftime("%d-%m-%y at %I:%M%p")
        print("Starting timed recording on ", full_datetime)
        
        if(mins_to_record < 60):
            time_lim = mins_to_record*60
            length_of_segment = mins_to_record*60
            print("will record for ", time_lim/60, "mins in ", length_of_segment/60, "-min increments")
        else:
            time_lim = mins_to_record*60
            length_of_segment = 60*60 #10-min segments if recording is more than 10min
            print("will record for ", time_lim/60, "mins in ", length_of_segment/60, "-min increments")

        filename = "TimedVideo_at_" + strftime("%H_%M_%S",localtime())
        foldername = path + "/" + filename + "/"
        print("foldername is", str(foldername))
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        
        if(not camera.closed):
            #do nothing if camera closed
            camera.close()
        with PiCamera() as mycamera:
            
            mycamera.framerate = 30
            
            mycamera.start_preview(fullscreen=False, window = (400, 100, 400, 200))
            sleep(2)
            
            mycamera.brightness = brightness
            mycamera.iso = ISO
            mycamera.contrast = contrast
            mycamera.exposure_compensation = exp_comp
            mycamera.saturation = saturation
            mycamera.sharpness = sharpness
            
            start =  time()
            for name in mycamera.record_sequence('%s%d_of_%d.h264' % (foldername,i,int(time_lim/length_of_segment)) for i in range(1, int(time_lim/length_of_segment)+1)):
                #with open((foldername + "camera_log_split.txt"), "a") as file:
                    #file.write("at time =" + time.strftime("%H:%M:%S",time.localtime()))
                    #file.write("\n\tRecording: " + name)
                print("\nat time =" , strftime("%H:%M:%S",localtime()))
                print("\n\tRecording: " + name)
                mycamera.wait_recording(length_of_segment)

        print("DONE")
        print("Time Elapsed is " + str(time()-start) + "seconds")
       
        print("Recording Complete!")

        sleep(2)
        return
    
    #function tp start timelapse photography based on user settings     
    def timelapse_on(self,mins_to_record,photo_freq,path):
        global camera
        global brightness
        global ISO
        global contrast
        global exp_comp
        global saturation
        global sharpness
        
        if(camera.closed):
            camera = PiCamera()
            
        mins_to_record = float(mins_to_record)
        photo_freq = float(photo_freq)
        print("Starting timelapse on ", strftime("%d-%m-%y at %I:%M:%S%p"))
        camera.start_preview(fullscreen=False, window = (400, 100, 400, 200))
        sleep(2)
        
        camera.brightness = brightness
        camera.iso = ISO
        camera.contrast = contrast
        camera.exposure_compensation = exp_comp
        camera.saturation = saturation
        camera.sharpness = sharpness
        
        t = 0
        photo_countdown = 0
        while t < mins_to_record*60:
            while photo_countdown < photo_freq:
                sleep(1)
                photo_countdown += 1 #increment time by 1 sec
                print("Timelapse in Progress - ",int((mins_to_record*60-t-photo_countdown)/3600), "h, ", int((mins_to_record*60-t-photo_countdown)%3600/60), "m, ", int((mins_to_record*60-t-photo_countdown)%3600%60), "s remaining \r",end='')
            photo_countdown = 0 #reset freq counter
            t += photo_freq #increment by photo_freq
            camera.capture(path  + "/" + 'TL_Photo_on_'+ strftime("%d_%m_%y_at_%I_%M_%S%p") + ".jpg")
        print("")
        print("")
        print("Timelapse Complete on ", strftime("%d-%m-%y at %I:%M:%S%p"))
        camera.stop_preview()
        sleep(2)
        return
    
    #the functions below use the sliders in the UI to set camera preferences to be used during recordings
    def set_brightness(self, value):
        global camera
        global brightness
        if(camera.closed):
            camera = PiCamera()
            
        if(camera.previewing == True):      
            print("setting brightness to: " + str(value))
            camera.brightness = int(value)
            brightness = int(value)
    def set_iso(self, value):
        global camera
        global ISO
        if(camera.closed):
            camera = PiCamera()
            
        if(camera.previewing == True):      
            print("setting iso to: " + str(value))
            camera.iso = int(value)
            ISO = int(value)
    def set_contrast(self, value):
        global camera
        global contrast
        if(camera.closed):
            camera = PiCamera()
            
        if(camera.previewing == True):      
            print("setting contrast to: " + str(value))
            camera.contrast = int(value)
            contrast = int(value)
    def set_exposure_compensation(self, value):
        global camera
        global exp_comp
        if(camera.closed):
            camera = PiCamera()
            
        if(camera.previewing == True):      
            print("setting exposure compensation to: " + str(value))
            camera.exposure_compensation = int(value)
            exp_comp = int(value)
    def set_saturation(self, value):
        global camera
        global saturation
        if(camera.closed):
            camera = PiCamera()
            
        if(camera.previewing == True):      
            print("setting saturation to: " + str(value))
            camera.saturation = int(value)
            saturation = int(value)
    def set_sharpness(self, value):
        global camera
        global saturation
        if(camera.closed):
            camera = PiCamera()
            
        if(camera.previewing == True):      
            print("setting sharpness to: " + str(value))
            camera.sharpness = int(value)
            sharpness = int(value)


class TestApp(App):
    def build(self):
        self.title = 'Mosquito Behavior Chamber - Control Panel'
        return ContainerFloat()
    
    

     
if __name__ == '__main__':
    TestApp().run()
