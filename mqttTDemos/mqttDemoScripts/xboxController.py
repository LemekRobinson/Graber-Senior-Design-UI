
#import serial
import time
import os
import pprint
import pygame

class xboxController(object):
    """Class representing the Xbox controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):

        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        """Listen for events to happen"""

        #button = ""
        #action = ""
        buttonAction = ''
        tempAction = ''
        #ser = serial.Serial('/dev/ttyACM0',9600)
        #print(ser.name)

        if not self.axis_data:
            self.axis_data = {}
            #Left Joystick L(0: -1.0) R(0: 1.0) U(1: -1.0) D(1: 1.0)
            #L2hold - 2:(-1.0 to 1.0)
            #Right Joystick L(3: -1.0) R(3: 1.0) U(4: -1.0) D(4: 1.0)
            #R2hold - 5:(-1.0 to 1.0)

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

                #Button Mapping
                #X - 0
                #O - 1
                #Triangle - 2
                #Square - 3
                #L1 - 4
                #R1 - 5
                #L2press - 6
                #R2press - 7
                #Share - 8
                #Options - 9
                #PS4 Home Btn - 10
                #Left Joystick Click - 11
                #Right Joystick Click - 12

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)
                self.hat_dataKeyCommands = {0:'L/R button hat',1:'U/D button hat'} #Thought this indexing was intuitive
                #Up - (0,1)
                #Down - (0,-1)
                #Left - (-1,0)
                #Right - (1,0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                    #Change action to whatever you want to happen hardware wise
                    if event.axis == 0 and self.axis_data[event.axis] > 0:
                        #"Left Joystick moved right"
                        buttonAction = 'Left Joystick moved right'
                    elif event.axis == 0 and self.axis_data[event.axis] < 0:
                        #button = "Left Joystick"
                        #action = "moved left"
                        buttonAction = 'Left Joystick moved left'
                    elif event.axis == 1 and self.axis_data[event.axis] > 0:
                        #button = "Left Joystick"
                        #action = "moved down"
                        buttonAction = 'Left Joystick moved down'
                    elif event.axis == 1 and self.axis_data[event.axis] < 0:
                        #button = "Left Joystick"
                        #action = "moved up"
                        buttonAction = 'Left Joystick moved up'
                    elif event.axis == 1 and self.axis_data[event.axis] == 0:
                        #Left Joystick moved to the center
                        buttonAction = 'Left Joystick moved to the center'
                    elif event.axis == 2 and self.axis_data[event.axis] < 0:
                        #button = "L2"
                        #action = "let go"
                        buttonAction = 'L2 let go'
                    elif event.axis == 2 and self.axis_data[event.axis] > 0:
                        #button = "L2"
                        #action = "pressed down"
                        buttonAction = 'L2 pressed down'
                    elif event.axis == 3 and self.axis_data[event.axis] < 0:
                        #button = "Right Joystick"
                        #action = "moved left"
                        buttonAction = 'Right Joystick moved left'
                    elif event.axis == 3 and self.axis_data[event.axis] > 0:
                        #button = "Right Joystick"
                        #action = "moved right"
                        buttonAction = 'Right Joystick moved right'
                    elif event.axis == 4 and self.axis_data[event.axis] > 0:
                        #button = "Right Joystick"
                        #action = "moved down"
                        buttonAction = 'Right Joystick moved down'
                    elif event.axis == 4 and self.axis_data[event.axis] < 0:
                        #button = "Right Joystick"
                        #action = "moved up"
                        buttonAction = 'Right Joystick moved up'
                    elif event.axis == 4 and self.axis_data[event.axis] == 0:
                        #Right Joystick moved to the center
                        buttonAction = 'Right Joystick moved to the center'
                    elif event.axis == 5 and self.axis_data[event.axis] < 0:
                        #button = "R2"
                        #action = "let go"
                        buttonAction = 'R2 let go'
                    elif event.axis == 5 and self.axis_data[event.axis] > 0:
                        #button = "R2"
                        #action = "pressed down"
                        buttonAction = 'R2 pressed down'

                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                    #Change action to whatever you want to happen hardware wise
                    if event.button == 0 and self.button_data[event.button] == True :
                        #button = "A button"
                        #action = "pressed"
                        buttonAction = 'A button pressed'
                    elif event.button == 1 and self.button_data[event.button] == True :
                        #button = "B button"
                        #action = "pressed"
                        buttonAction = 'B button pressed'
                    elif event.button == 2 and self.button_data[event.button] == True :
                        #button = "X button"
                        #action = "pressed"
                        buttonAction = 'X button pressed'
                    elif event.button == 3 and self.button_data[event.button] == True :
                        #button = "Y button"
                        #action = "pressed"
                        buttonAction = 'Y button pressed'
                    elif event.button == 4 and self.button_data[event.button] == True :
                        #button = "L1 button"
                        #action = "pressed"
                        buttonAction = 'L1 button pressed'
                    elif event.button == 5 and self.button_data[event.button] == True :
                        #button = "R1 button"
                        #action = "pressed"
                        buttonAction = 'R1 button pressed'
                    elif event.button == 6 and self.button_data[event.button] == True :
                        #button = "L2 button"
                        #action = "pressed"
                        buttonAction = 'L2 button pressed'
                    elif event.button == 7 and self.button_data[event.button] == True :
                        #button = "R2 button"
                        #action = "pressed"
                        buttonAction = 'R2 button pressed'
                    elif event.button == 8 and self.button_data[event.button] == True :
                        #button = "Xbox button"
                        #action = "pressed"
                        buttonAction = 'Xbox button pressed'
                    elif event.button == 9 and self.button_data[event.button] == True :
                        #button = "Options button"
                        #action = "pressed"
                        buttonAction = 'Left Joystick button pressed'
                    elif event.button == 10 and self.button_data[event.button] == True :
                        #button = "PS4 Home button"
                        #action = "pressed"
                        buttonAction = 'Right Joystick button pressed'
                    elif event.button == 11 and self.button_data[event.button] == True :
                        #button = "Left Joystick button"
                        #action = "pressed"
                        buttonAction = 'Left Joystick button pressed'
                    elif event.button == 12 and self.button_data[event.button] == True :
                        #button = "Right Joystick button"
                        #action = "pressed"
                        buttonAction = 'Right Joystick button pressed'
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                    #Placed the print command inside the if else so that the event member was defined
                    #pprint.pprint(self.button_dataKeyCommandsRelease[int(event.button)])
                    if event.button == 0 and self.button_data[event.button] == False :
                        #button = "A button"
                        #action = "let go"
                        buttonAction = 'A button let go'
                    elif event.button == 1 and self.button_data[event.button] == False :
                        #button = "B button"
                        #action = "let go"
                        buttonAction = 'B button let go'
                    elif event.button == 2 and self.button_data[event.button] == False :
                        #button = "X button"
                        #action = "let go"
                        buttonAction = 'X button let go'
                    elif event.button == 3 and self.button_data[event.button] == False :
                        #button = "Y button"
                        #action = "let go"
                        buttonAction = 'Y button let go'
                    elif event.button == 4 and self.button_data[event.button] == False :
                        #button = "L1 button"
                        #action = "let go"
                        buttonAction = 'L1 button let go'
                    elif event.button == 5 and self.button_data[event.button] == False :
                        #button = "R1 button"
                        #action = "let go"
                        buttonAction = 'R1 button let go'
                    elif event.button == 6 and self.button_data[event.button] == False :
                        #button = "L2 button"
                        #action = "let go"
                        buttonAction = 'L2 button let go'
                    elif event.button == 7 and self.button_data[event.button] == False :
                        #button = "R2 button"
                        #action = "let go"
                        buttonAction = 'R2 button let go'
                    elif event.button == 8 and self.button_data[event.button] == False :
                        #button = "Xbox button"
                        #action = "let go"
                        buttonAction = 'Xbox button let go'
                    elif event.button == 9 and self.button_data[event.button] == False :
                        #button = "Options button"
                        #action = "let go"
                        buttonAction = 'Left Joystick button let go'
                    elif event.button == 10 and self.button_data[event.button] == False :
                        #button = "PS4 Home button"
                        #action = "let go"
                        buttonAction = 'Right Joystick button let go'
                    elif event.button == 11 and self.button_data[event.button] == False :
                        #button = "Left Joystick button"
                        #action = "let go"
                        buttonAction = 'Left Joystick button let go'
                    elif event.button == 12 and self.button_data[event.button] == False :
                        #button = "Right Joystick button"
                        #action = "let go"
                        buttonAction = 'Right Joystick button let go'

                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value
                    #Change action to whatever you want to happen hardware wise
                    if event.value == (1,0):
                        #button = "Right Button"
                        #action = "was pressed"
                        buttonAction = 'Right button pressed'
                    elif event.value == (-1,0):
                        #button = "Left Button"
                        #action = "was pressed"
                        buttonAction = 'Left Button was pressed'
                    elif event.value == (0,-1):
                        #button = "Down Button"
                        #action = "was pressed"
                        buttonAction = 'Down button was pressed'
                    elif event.value == (0,1):
                        #button = "Up Button"
                        #action = "was pressed"
                        buttonAction = 'Up button was pressed'
                    elif event.value == (0,0):
                        #Stops all motion
                        buttonAction = 'Everything was released'


                #pprint.pprint("%s was %s."%(button,action))
                #controllerAction = button + ' ' +  action
                client.loop_start()
                controllerAction = buttonAction
                #if tempAction != controllerAction:
                client.publish(topic,controllerAction)
                #tempAction = controllerAction
                #else:
                    #time.sleep(0.3)
                    #lient.publish('z')
                #	tempAction = buttonAction
                #else:
                #    print(tempAction,buttonAction)
                #print(controllerAction)   #left for debugging purposes
                #read_val = ser.read_until(controllerAction,1)
                #print read_val

                #Happens exteremely fast. So you may have to turn off the clear function to view it.
                #os.system('clear')
                #pprint.pprint(self.button_data)
                #pprint.pprint(self.axis_data)
                #pprint.pprint(self.hat_data)
                client.loop_stop()
