from picamera import PiCamera
from time import sleep
from time import strftime


#folder selection
folder = "/home/pi/Desktop/" 


camera = PiCamera()




#preview button on: WORKS
#camera.start_preview()
#sleep(2)


#preview button off: WORKS
#camera.stop_preview()
#sleep(2)

#photo button clicked: WORKS
#full_datetime = strftime("%d-%m-%y at %I:%M%p")
#filename = 'Photo on '+ full_datetime + ".jpg"
#camera.start_preview()
#sleep(2)
#camera.capture(folder  + filename)
#camera.stop_preview()


#record button on: WORKS
#full_datetime = strftime("%d-%m-%y at %I:%M%p")
#filename = 'Video on '+ full_datetime + ".h264"
#camera.start_preview()
#camera.start_recording(folder  + filename)
#sleep(2)

#record button off: WORKS
#camera.stop_recording()
#camera.stop_preview()

#timed recording: WORKS
#record_duration = 2 #set by user, units are minutes
#full_datetime = strftime("%d-%m-%y at %I:%M%p")
#filename = 'Video on '+ full_datetime + ".h264"
#camera.start_preview()
#camera.start_recording(folder  + filename)
#sleep(record_duration*60)
#camera.stop_recording()
#camera.stop_preview()



