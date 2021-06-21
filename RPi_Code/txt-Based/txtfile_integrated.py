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

#for txtfile parsing
import time
import os.path
import configparser

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

def LED1_on():
    led1.on()
def LED2_on():
    led2.on()
def LED3_on():
    led3.on()
    
def LED1_off():
    led1.off()
def LED2_off():
    led2.off()
def LED3_off():
    led3.off()

#opens preview when preview button is clicked. Closes existing preview window (if it exists) and opens a new one
def preview_on():
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

def preview_off():
    global camera
    if(camera.closed):
        camera = PiCamera()
    print("turning preview off")
    camera.stop_preview()

#initiates manual recording. This function is called on both ends of the manual recording (to start and stop it)
def record_toggle(path):
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
def timed_record_on(mins_to_record,path):
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
        
        start =  time.time()
        for name in mycamera.record_sequence('%s%d_of_%d.h264' % (foldername,i,int(time_lim/length_of_segment)) for i in range(1, int(time_lim/length_of_segment)+1)):
            #with open((foldername + "camera_log_split.txt"), "a") as file:
                #file.write("at time =" + time.strftime("%H:%M:%S",time.localtime()))
                #file.write("\n\tRecording: " + name)
            print("\nat time =" , strftime("%H:%M:%S",localtime()))
            print("\n\tRecording: " + name)
            mycamera.wait_recording(length_of_segment)

    print("DONE")
    print("Time Elapsed is " + str(time.time()-start) + "seconds")
   
    print("Recording Complete!")
    camera.close()
    sleep(2)
    return

#function tp start timelapse photography based on user settings     
def timelapse_on(mins_to_record,photo_freq,path):
    global camera
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
def set_brightness(value):
    global camera
    if(camera.closed):
        camera = PiCamera()
        
    if(camera.previewing == True):      
        print("setting brightness to: " + str(value))
        camera.brightness = int(value)
        brightness = int(value)

def set_iso(value):
    global camera
    if(camera.closed):
        camera = PiCamera()
        
    if(camera.previewing == True):      
        print("setting iso to: " + str(value))
        camera.iso = int(value)
        ISO = int(value)

def set_contrast(value):
    global camera
    if(camera.closed):
        camera = PiCamera()
        
    if(camera.previewing == True):      
        print("setting contrast to: " + str(value))
        camera.contrast = int(value)
        contrast = int(value)

def set_exposure_compensation(value):
    global camera
    if(camera.closed):
        camera = PiCamera()
        
    if(camera.previewing == True):      
        print("setting exposure compensation to: " + str(value))
        camera.exposure_compensation = int(value)
        exp_comp = int(value)

def set_saturation(value):
    global camera
    if(camera.closed):
        camera = PiCamera()
        
    if(camera.previewing == True):      
        print("setting saturation to: " + str(value))
        camera.saturation = int(value)
        saturation = int(value)

def set_sharpness(value):
    global camera
    if(camera.closed):
        camera = PiCamera()
        
    if(camera.previewing == True):      
        print("setting sharpness to: " + str(value))
        camera.sharpness = int(value)
        sharpness = int(value)


###################### CODE STARTS HERE ###########
folder = "/home/pi/Desktop/" #default location to save videos & images
example_filename = '/home/pi/Desktop/example_config.txt'
total_recording_length_mins = 180

config = configparser.ConfigParser()
config['camera_settings'] = {'brightness':brightness, 'ISO':ISO, 'contrast': contrast, 'exp_comp': exp_comp, 'saturation': saturation, 'sharpness':sharpness}
#config['led_settings'] = {'led1':'off', 'led2':'off', 'led3':'off'}
config['record_settings'] = {'total_recording_length_mins':total_recording_length_mins}
config['saveout'] = {'savefolder':'/home/pi/Desktop/'}

with open('/home/pi/Desktop/example_config.txt', 'w') as configfile:
    config.write(configfile)
    
print("Welcome to the text_input video recorder. The following default configuration file has been created for your reference:")
print(example_filename + '\n')
print("To use the system with these default settings, enter the same filepath below. \nOtherwise, create a copy of that file, modify the settings and enter the new config filename below:")
input_filename = input("\n")
print("You entered: " + input_filename)

if(os.path.isfile(input_filename)):
    print("The entered filename (" + input_filename + ") is valid! Opening now")
    config.read(input_filename)
    print("brightness: " + config['camera_settings']['brightness'])
    print("ISO: " + config['camera_settings']['ISO'])
    print("contrast: " + config['camera_settings']['contrast'])
    print("exp_comp: " + config['camera_settings']['exp_comp'])
    print("saturation: " + config['camera_settings']['saturation'])
    print("sharpness: " + config['camera_settings']['sharpness'])
    print("\ntotal_recording_length_mins: " + config['record_settings']['total_recording_length_mins'])
    print("\nsavefolder: " + config['saveout']['savefolder'] + "\n")
    #brightness = int(config['camera_settings']['brightness'])
    ISO = int(config['camera_settings']['ISO'])
    contrast = int(config['camera_settings']['contrast'])
    exp_comp = int(config['camera_settings']['exp_comp'])
    saturation = int(config['camera_settings']['saturation'])
    sharpness = int(config['camera_settings']['sharpness'])
    total_recording_length_mins = int(config['record_settings']['total_recording_length_mins'])
    input_folder = config['saveout']['savefolder']
    if(os.path.isdir(input_folder)):
        print("The saveout folder provided in the config file (" + input_folder + ") is valid. Outputs will be saved there.")
        folder = input_folder
    else:
        print("The saveout folder provided in the config file (" + input_folder + ") is invalid. Outputs will be saved to the default folder instead (" + folder + ")")
else:
    print("The entered config filepath (" + input_filename + ") is invalid!\n")
        

time.sleep(2)
print("Starting recording...")
#run timed_recording here
preview_on()
time.sleep(1)
timed_record_on(total_recording_length_mins, folder)
print("Recording complete!")
preview_off()
