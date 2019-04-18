import clientObjClass as cli
import controlPublisher as controlPub
import pdb
import time
import serial
import random

broker = '143.215.99.102' #Always change this to the ip address sending the info
port = 1883
topic = 'controllerTest'
tracker = 0
sensorData = ''

cliePub = controlPub.controlPublisher()

cliePub.buildPublisher()
cliePub.addPublisherParams(broker,port,topic)

cliePub.connectPublisher()

d = cliePub.checkConnection()
c = cliePub.checkClientDetails()

print("Publisher details")
print(c)
print("Publisher is connected: ")
print(d)
pubClient = cliePub.getClient()
print(pubClient)
print('Here in the publisher')

cliePub.initController()
cliePub.actionTypeCreator()

while True:

    mvmntData = cliePub.actionIdentifier()

    print('Sending mvmnt data to the subscriber')
    print('\n')

    if mvmntData == None:
        mvmntData = 'W' #Wait condition


    print(mvmntData)
    time.sleep(0.5)
    status = cliePub.publishMvmnt(mvmntData)
    print('Data published')
    #tracker += 1
    #print('At ' + str(tracker) + ' second ' + str(status))
    #newData = cliePub.parseGuiData(sensorData)
    #print('Data parsed into dictionary')
    #print(newData)
    #print('\n')

cliePub.foreverLoopClient()


#cliePub.stopPublishLoop()
