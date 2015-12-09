#!/usr/bin/env python
#
# joystick-servo.py
#
# created 19 December 2007
# copyleft 2007 Brian D. Wendt
# http://principialabs.com/
#
# code adapted from:
# http://svn.lee.org/swarm/trunk/mothernode/python/multijoy.py
#
# NOTE: This script requires the following Python modules:
#  pyserial - http://pyserial.sourceforge.net/
#  pygame   - http://www.pygame.org/
# Win32 users may also need:
#  pywin32  - http://sourceforge.net/projects/pywin32/
#

import serial
import pygame
import socket
import servo

# allow multiple joysticks 
joy = []

# use flags
global screwtog
screwtog = 1
global wheeltog
wheeltog = 1

# Arduino USB port address (try "COM5" on Win32)
# usbport = "COM32"

# define usb serial connection to Arduino

# ser = serial.Serial(usbport, 9600)

# handle joystick event
def handleJoyEvent(e):
    
    if e.type == pygame.JOYAXISMOTION:
        axis = "unknown"
        if (e.dict['axis'] == 1):
            axis = "X"

        if (e.dict['axis'] == 0):
            axis = "Y"

        if (e.dict['axis'] == 2):
            axis = "Throttle"

        if (e.dict['axis'] == 3):
            axis = "Z"

        joystick = e.dict['joy']

        if (axis != "unknown"):
            str = "Axis: %s; Value: %f" % (axis, e.dict['value'])
            # uncomment to debug
            #output(str, e.dict['joy'])
            
            pos = e.dict['value']
            move = round(pos * 90, 0)*3/5
            serv = int((move/2) + 90)

            # X Axis on Stick1
            if ((axis == "X") and (joystick == 0)):
                servo.move(client_socket, 1, serv)
            # X Axis on Stick2
            if ((axis == "X") and (joystick == 1)):
                servo.move(client_socket, 2, serv)
            
            # Twist on Stick1
            #if ((axis == "Z") and (joystick == 0) and screwtog==1):
            #    servo.move(client_socket, 3, serv)
            # Lever on Stick1
            if ((axis == "Throttle") and (joystick == 0) and wheeltog==1):
                # Lever when down is stop, lever when up is full forward
                pos = 1 - pos
                move = round(pos * 45, 0)
                serv = int((move/2) + 90)
                servo.move(client_socket, 4, serv)
                    
    #Bucket stop
    elif e.type == pygame.JOYBUTTONUP:
        str = "Button: %d" % (e.dict['button'])
        if ((e.dict['button'] == 5)):
            servo.move(client_socket, 5, 90)
            #upEndTime = time.time()
            #timeDiff = upEndTime - upStartTime
            #print "%d seconds" % timeDiff
            print "Bucket stopped"
        if ((e.dict['button'] == 3)):
            servo.move(client_socket, 5, 90)
            #downEndTime = time.time()
            #timeDiff = downEndTime - downStartTime
            #print "%d seconds" % timeDiff
            print "Bucket stopped"
        if ((e.dict['button'] == 4)):
        #    if(timeTaken == 0):
        #        timeTaken = timeStart - time.time()
        #    else:
        #        timeTaken += time.time() - timeStart
            servo.move(client_socket, 3, 90)

        if ((e.dict['button'] == 2)):
        #    if(timeTaken == 0):
        #        timeTaken = timeStart - time.time()
        #    else:
        #        timeTaken += time.time() - timeStart
            servo.move(client_socket, 3, 90)

    elif e.type == pygame.JOYBUTTONDOWN:
        str = "Button: %d" % (e.dict['button'])
        # uncomment to debug
        #output(str, e.dict['joy'])
        if (e.dict['button'] == 1):
            servo.move(client_socket, 3, 90)
            print "Screw off"
        if (e.dict['button'] == 8):
            if (wheeltog == 1):
                global wheeltog
                wheeltog = 0
                servo.move(client_socket, 4, 90)
                print "Wheel off"
            else:
                global wheeltog
                wheeltog = 1
                #pos = joy[1].get_axis(3);
                #move = round(pos * 90, 0)
                #serv = int((move/2) + 90)
                #servo.move(client_socket, 4, serv);
                print "Wheel on"
        # Wheel up
        if (e.dict['button'] == 5):
            servo.move(client_socket, 5, 45)
        # Wheel down
        if (e.dict['button'] == 3):
            servo.move(client_socket, 5, 135)
        # Bucket up
        if ((e.dict['button'] == 4)):
            servo.move(client_socket, 3, 45)
            print "Dumping"
        # Bucket down
        if ((e.dict['button'] == 2)):
            servo.move(client_socket, 3, 135)
            print "Returning"
        # Button 0 (trigger) to quit
        if (e.dict['button'] == 0):
            print "Bye!\n"
            # ser.close()
            quit()
            
    else:
        pass

# print the joystick position
def output(line, stick):
    print "Joystick: %d; %s" % (stick, line)

# wait for joystick input
def joystickControl():
    while True:
        e = pygame.event.wait()
        if (e.type == pygame.JOYAXISMOTION or e.type == pygame.JOYBUTTONDOWN or e.type==pygame.JOYBUTTONUP):
            handleJoyEvent(e)

# main method
def main():

    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # initialize pygame
    pygame.joystick.init()
    pygame.display.init()
    if not pygame.joystick.get_count():
        print "\nPlease connect a joystick and run again.\n"
        quit()
    print "\n%d joystick(s) detected." % pygame.joystick.get_count()
    for i in range(pygame.joystick.get_count()):
        myjoy = pygame.joystick.Joystick(i)
        myjoy.init()
        joy.append(myjoy)
        print "Joystick %d: " % (i) + joy[i].get_name()
    print "Depress trigger (button 0) to quit.\n"

    # run joystick listener loop
    joystickControl()

    client_socket.close()


# allow use as a module or standalone script
if __name__ == "__main__":
    main()
