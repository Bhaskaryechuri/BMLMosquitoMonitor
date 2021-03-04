from time import sleep
from time import strftime
from picamera import PiCamera


camera = PiCamera()
folder = "/home/pi/Desktop/" 


"""
from time import sleep


mins_to_record = 60.01
t = 0
while t <= mins_to_record*60:
    print("Recording in Progress - ",int((mins_to_record*60-t)/3600), "h, ", int((mins_to_record*60-t)%3600/60), "m, ", int((mins_to_record*60-t)%3600%60), "s remaining \r",end='')
    sleep(1)
    t+=1 #increment seconds
print("Complete!")

"""
mins_to_record = 0.25
photo_freq = 5
print("Starting timelapse on ", strftime("%d-%m-%y at %I:%M:%S%p"))
camera.start_preview(fullscreen=False, window = (400, 100, 400, 200))
t = 0
photo_countdown = 0
while t < mins_to_record*60:
    while photo_countdown < photo_freq:
        sleep(1)
        photo_countdown += 1 #increment time by 1 sec
        print("Timelapse in Progress - ",int((mins_to_record*60-t-photo_countdown)/3600), "h, ", int((mins_to_record*60-t-photo_countdown)%3600/60), "m, ", int((mins_to_record*60-t-photo_countdown)%3600%60), "s remaining \r",end='')
    photo_countdown = 0 #reset freq counter
    t += photo_freq #increment by photo_freq
    camera.capture(folder + 'Photo on '+ strftime("%d-%m-%y at %I:%M:%S%p") + ".jpg")
print("")
print("")
print("Timelapse Complete on ", strftime("%d-%m-%y at %I:%M:%S%p"))
camera.stop_preview()
    
