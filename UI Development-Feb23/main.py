#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 13:25:26 2020

@author: bhaskar
"""
#for gpio stuff
import sys
import os
from gpiozero import LED
from time import sleep
from time import strftime
from time import localtime
from time import time
import psutil

led1 = LED(3)
led2 = LED(27)
led3 = LED(10)


#for camera stuff
from picamera import PiCamera
from time import sleep
from time import strftime

camera = PiCamera()
folder = "/home/pi/Desktop/" 

#for kivy stuff
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout




class ContainerFloat(FloatLayout):    
    def __init__(self, **kwargs):
        super(ContainerFloat, self).__init__(**kwargs)
        global camera
        if(camera.closed):
            camera = PiCamera()
    
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


    def preview_on(self):
        global camera
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
    
    
    def record_toggle(self,path):
        global camera
        if(camera.closed):
            camera = PiCamera()
            
        if camera.recording == True:
            print("stopping the recording")
            camera.stop_recording()
            camera.stop_preview()
            sleep(2)
        else:
            print("starting to record")
            full_datetime = strftime("%d-%m-%y at %I:%M%p")
            filename = 'Video on '+ full_datetime + ".h264"
            camera.start_preview(fullscreen=False, window = (400, 100, 400, 200))
            camera.start_recording(path  + "/"+ filename)
            sleep(2)
        return
    
        
    def timed_record_on(self,mins_to_record,path):
        global camera
        if(camera.closed):
            camera = PiCamera()
            
        #global camera
        mins_to_record = float(mins_to_record)
        full_datetime = strftime("%d-%m-%y at %I:%M%p")
        print("Starting to record on ", full_datetime)
        #print("Memory available = " + str(psutil.disk_usage('/').free/1024/1024/1024))
        #if((psutil.disk_usage('/').free/1024/1024/1024)<1): #if less than 1GB, dont record
        #    print("LOW ON MEMORY, CANNOT RECORD MORE VIDEO")
        #    return
        #filename = 'Video on '+ full_datetime + ".h264"
        #print("File name: " + path + filename)
        #camera.start_preview(fullscreen=False, window = (400, 100, 400, 200))
        #camera.start_recording(path  + "/"+ filename)
        #sleep(2)

        ####
        if(mins_to_record < 60):
            time_lim = mins_to_record*60
            length_of_segment = mins_to_record*60
        else:
            time_lim = mins_to_record*60
            length_of_segment = 60*60 #10-min segments if recording is more than 10min
        filename = "video_at_" + strftime("%H:%M:%S",localtime())
        foldername = '/home/pi/Desktop/' + filename + "/"
        print("foldername is", str(foldername))
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        
        if(not camera.closed):
            #do nothing if camera closed
            camera.close()
        with PiCamera() as mycamera:
            mycamera.start_preview(fullscreen=False, window = (400, 100, 400, 200))
            sleep(2)
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
        ####

        #t = 0
        #while t <= mins_to_record*60:
        #    print("Recording in Progress - ",int((mins_to_record*60-t)/3600), "h, ", int((mins_to_record*60-t)%3600/60), "m, ", int((mins_to_record*60-t)%3600%60), "s remaining \r",end='')
        #    sleep(1)
        #    t+=1 #increment seconds
        #print("")
        print("Recording Complete!")
        #camera.stop_recording()
        #camera.stop_preview()
        sleep(2)
        return
        
    def timelapse_on(self,mins_to_record,photo_freq,path):
        global camera
        if(camera.closed):
            camera = PiCamera()
            
        mins_to_record = float(mins_to_record)
        photo_freq = float(photo_freq)
        print("Starting timelapse on ", strftime("%d-%m-%y at %I:%M:%S%p"))
        camera.start_preview(fullscreen=False, window = (400, 100, 400, 200))
        sleep(2)
        t = 0
        photo_countdown = 0
        while t < mins_to_record*60:
            while photo_countdown < photo_freq:
                sleep(1)
                photo_countdown += 1 #increment time by 1 sec
                print("Timelapse in Progress - ",int((mins_to_record*60-t-photo_countdown)/3600), "h, ", int((mins_to_record*60-t-photo_countdown)%3600/60), "m, ", int((mins_to_record*60-t-photo_countdown)%3600%60), "s remaining \r",end='')
            photo_countdown = 0 #reset freq counter
            t += photo_freq #increment by photo_freq
            camera.capture(path  + "/" + 'Photo on '+ strftime("%d-%m-%y at %I:%M:%S%p") + ".jpg")
        print("")
        print("")
        print("Timelapse Complete on ", strftime("%d-%m-%y at %I:%M:%S%p"))
        camera.stop_preview()
        sleep(2)
        return
        
    def set_brightness(self, value):
        global camera
        if(camera.closed):
            camera = PiCamera()
            
        if(camera.previewing == True):      
            print("setting brightness to: " + str(value))
            camera.brightness = int(value)
    def set_iso(self, value):
        global camera
        if(camera.closed):
            camera = PiCamera()
            
        if(camera.previewing == True):      
            print("setting iso to: " + str(value))
            camera.iso = int(value)
    def set_contrast(self, value):
        global camera
        if(camera.closed):
            camera = PiCamera()
            
        if(camera.previewing == True):      
            print("setting contrast to: " + str(value))
            camera.contrast = int(value)
    def set_exposure_compensation(self, value):
        global camera
        if(camera.closed):
            camera = PiCamera()
            
        if(camera.previewing == True):      
            print("setting exposure compensation to: " + str(value))
            camera.exposure_compensation = int(value)
    def set_saturation(self, value):
        global camera
        if(camera.closed):
            camera = PiCamera()
            
        if(camera.previewing == True):      
            print("setting saturation to: " + str(value))
            camera.saturation = int(value)
    def set_sharpness(self, value):
        global camera
        if(camera.closed):
            camera = PiCamera()
            
        if(camera.previewing == True):      
            print("setting sharpness to: " + str(value))
            camera.sharpness = int(value)
 
class TestApp(App):
    def build(self):
        self.title = 'Mosquito Behavior Chamber - Control Panel'
        return ContainerFloat()
    
    

     
if __name__ == '__main__':
    TestApp().run()
