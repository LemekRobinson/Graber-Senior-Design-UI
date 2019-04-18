import clientObjClass as cli
import pdb
import time
import random
import pprint
import os
import pygame


class controlPublisher(object):

    def __init__(self):
        self.__connectionStatus = False
        clientObj = cli.clientObjClass()
        self.__clientObj = clientObj
        self.controller = None
        self.__axis_data = None
        self.__hat_data = None
        self.__button_data = None
        self.__hat_dataKeyCommands = None
        self.__button_data = None


        #self.__sensorDataPreParse = ''
        #self.__sensorDataPostParse = {'AirQualitySensor': '', 'InfraredTempSensor' : '', 'GasContentSensor' : ''}

    def getClient(self):
        a = self.__clientObj.getClient()
        return(a)

    def buildPublisher(self):
        self.__clientObj.createClient()

    def addPublisherParams(self,broker,port,topic):
        self.__clientObj.setClientParams(broker,port,topic)

    def connectPublisher(self):
        self.__clientObj.connectClient()
        self.__connectionStatus = True

    def startPublishLoop(self,indicator):
        self.__clientObj.subscribeToTopic()
        status = self.__clientObj.startLoop(indicator)

    def stopPublishLoop(self):
        status = self.__clientObj.endLoop()

    def publishMvmnt(self,data):
        print('Assigned Actuator Data')
        a = self.__clientObj.publishData(data)
        return(a)

    def initController(self):
        #Initializing the joystick components
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def actionTypeCreator(self):

        if not self.__axis_data:
            self.__axis_data = {}

        if not self.__button_data:
            self.__button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.__button_data[i] = False

        if not self.__hat_data:
            self.__hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.__hat_data[i] = (0, 0)
                self.__hat_dataKeyCommands = {0:'L/R button hat',1:'U/D button hat'}

    def actionIdentifier(self):
        buttonAction = ''
        tempAction = ''

        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.__axis_data[event.axis] = round(event.value,2)
                #Change action to whatever you want to happen hardware wise
                if event.axis == 0 and self.__axis_data[event.axis] > 0:
                    #"Left Joystick moved right"
                    buttonAction = 'Left Joystick moved right'
                elif event.axis == 0 and self.__axis_data[event.axis] < 0:
                    #button = "Left Joystick"
                    #action = "moved left"
                    buttonAction = 'Left Joystick moved left'
                elif event.axis == 1 and self.__axis_data[event.axis] > 0:
                    #button = "Left Joystick"
                    #action = "moved down"
                    buttonAction = 'Left Joystick moved down'
                elif event.axis == 1 and self.__axis_data[event.axis] < 0:
                    #button = "Left Joystick"
                    #action = "moved up"
                    buttonAction = 'Left Joystick moved up'
                elif event.axis == 1 and self.__axis_data[event.axis] == 0:
                    #Left Joystick moved to the center
                    buttonAction = 'Left Joystick moved to the center'
                elif event.axis == 2 and self.__axis_data[event.axis] < 0:
                    #button = "L2"
                    #action = "let go"
                    buttonAction = 'L2 let go'
                elif event.axis == 2 and self.__axis_data[event.axis] > 0:
                    #button = "L2"
                    #action = "pressed down"
                    buttonAction = 'L2 pressed down'
                elif event.axis == 3 and self.__axis_data[event.axis] < 0:
                    #button = "Right Joystick"
                    #action = "moved left"
                    buttonAction = 'Right Joystick moved left'
                elif event.axis == 3 and self.__axis_data[event.axis] > 0:
                    #button = "Right Joystick"
                    #action = "moved right"
                    buttonAction = 'Right Joystick moved right'
                elif event.axis == 4 and self.__axis_data[event.axis] > 0:
                    #button = "Right Joystick"
                    #action = "moved down"
                    buttonAction = 'Right Joystick moved down'
                elif event.axis == 4 and self.__axis_data[event.axis] < 0:
                    #button = "Right Joystick"
                    #action = "moved up"
                    buttonAction = 'Right Joystick moved up'
                elif event.axis == 4 and self.__axis_data[event.axis] == 0:
                    #Right Joystick moved to the center
                    buttonAction = 'Right Joystick moved to the center'
                elif event.axis == 5 and self.__axis_data[event.axis] < 0:
                    #button = "R2"
                    #action = "let go"
                    buttonAction = 'R2 let go'
                elif event.axis == 5 and self.__axis_data[event.axis] > 0:
                    #button = "R2"
                    #action = "pressed down"
                    buttonAction = 'R2 pressed down'

            elif event.type == pygame.JOYBUTTONDOWN:
                self.__button_data[event.button] = True
                #Change action to whatever you want to happen hardware wise
                if event.button == 0 and self.__button_data[event.button] == True :
                    #button = "A button"
                    #action = "pressed"
                    buttonAction = 'A button pressed'
                elif event.button == 1 and self.__button_data[event.button] == True :
                    #button = "B button"
                    #action = "pressed"
                    buttonAction = 'B button pressed'
                elif event.button == 2 and self.__button_data[event.button] == True :
                    #button = "X button"
                    #action = "pressed"
                    buttonAction = 'X button pressed'
                elif event.button == 3 and self.__button_data[event.button] == True :
                    #button = "Y button"
                    #action = "pressed"
                    buttonAction = 'Y button pressed'
                elif event.button == 4 and self.__button_data[event.button] == True :
                    #button = "L1 button"
                    #action = "pressed"
                    buttonAction = 'L1 button pressed'
                elif event.button == 5 and self.__button_data[event.button] == True :
                    #button = "R1 button"
                    #action = "pressed"
                    buttonAction = 'R1 button pressed'
                elif event.button == 6 and self.__button_data[event.button] == True :
                    #button = "L2 button"
                    #action = "pressed"
                    buttonAction = 'L2 button pressed'
                elif event.button == 7 and self.__button_data[event.button] == True :
                    #button = "R2 button"
                    #action = "pressed"
                    buttonAction = 'R2 button pressed'
                elif event.button == 8 and self.__button_data[event.button] == True :
                    #button = "Xbox button"
                    #action = "pressed"
                    buttonAction = 'Xbox button pressed'
                elif event.button == 9 and self.__button_data[event.button] == True :
                    #button = "Options button"
                    #action = "pressed"
                    buttonAction = 'Left Joystick button pressed'
                elif event.button == 10 and self.__button_data[event.button] == True :
                    #button = "PS4 Home button"
                    #action = "pressed"
                    buttonAction = 'Right Joystick button pressed'
                elif event.button == 11 and self.__button_data[event.button] == True :
                    #button = "Left Joystick button"
                    #action = "pressed"
                    buttonAction = 'Left Joystick button pressed'
                elif event.button == 12 and self.__button_data[event.button] == True :
                    #button = "Right Joystick button"
                    #action = "pressed"
                    buttonAction = 'Right Joystick button pressed'
            elif event.type == pygame.JOYBUTTONUP:
                self.__button_data[event.button] = False
                #Placed the print command inside the if else so that the event member was defined
                #pprint.pprint(self.__button_dataKeyCommandsRelease[int(event.button)])
                if event.button == 0 and self.__button_data[event.button] == False :
                    #button = "A button"
                    #action = "let go"
                    buttonAction = 'A button let go'
                elif event.button == 1 and self.__button_data[event.button] == False :
                    #button = "B button"
                    #action = "let go"
                    buttonAction = 'B button let go'
                elif event.button == 2 and self.__button_data[event.button] == False :
                    #button = "X button"
                    #action = "let go"
                    buttonAction = 'X button let go'
                elif event.button == 3 and self.__button_data[event.button] == False :
                    #button = "Y button"
                    #action = "let go"
                    buttonAction = 'Y button let go'
                elif event.button == 4 and self.__button_data[event.button] == False :
                    #button = "L1 button"
                    #action = "let go"
                    buttonAction = 'L1 button let go'
                elif event.button == 5 and self.__button_data[event.button] == False :
                    #button = "R1 button"
                    #action = "let go"
                    buttonAction = 'R1 button let go'
                elif event.button == 6 and self.__button_data[event.button] == False :
                    #button = "L2 button"
                    #action = "let go"
                    buttonAction = 'L2 button let go'
                elif event.button == 7 and self.__button_data[event.button] == False :
                    #button = "R2 button"
                    #action = "let go"
                    buttonAction = 'R2 button let go'
                elif event.button == 8 and self.__button_data[event.button] == False :
                    #button = "Xbox button"
                    #action = "let go"
                    buttonAction = 'Xbox button let go'
                elif event.button == 9 and self.__button_data[event.button] == False :
                    #button = "Options button"
                    #action = "let go"
                    buttonAction = 'Left Joystick button let go'
                elif event.button == 10 and self.__button_data[event.button] == False :
                    #button = "PS4 Home button"
                    #action = "let go"
                    buttonAction = 'Right Joystick button let go'
                elif event.button == 11 and self.__button_data[event.button] == False :
                    #button = "Left Joystick button"
                    #action = "let go"
                    buttonAction = 'Left Joystick button let go'
                elif event.button == 12 and self.__button_data[event.button] == False :
                    #button = "Right Joystick button"
                    #action = "let go"
                    buttonAction = 'Right Joystick button let go'

            elif event.type == pygame.JOYHATMOTION:
                self.__hat_data[event.hat] = event.value
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

            if tempAction != buttonAction: #substring changed to let go and moved to center
                output = buttonAction
                tempAction = buttonAction
            else:
                time.sleep(0.3)
                output = 'Sleep'
                tempAction = buttonAction

            return(output)

    def checkConnection(self):
        return(self.__connectionStatus)

    def checkClientDetails(self):
        details = self.__clientObj.getClientParams()
        return(details)

    def foreverLoopClient(self):
        self.__clientObj.loopClientForever()
