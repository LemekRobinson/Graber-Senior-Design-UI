import clientObjClass as cli
import guiPublisher as guiPub
import pdb
import time
import serial
import random

broker = '143.215.99.102' #Always change this to the ip address sending the info
port = 1883
topic = 'guiParseTest'
tracker = 0
sensorData = ''

cliePub = guiPub.guiPublisher()

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


while True:
    #Replace this (below) with the serial reading of the port for the sensor data


#def serialReceiving(self):
#    while True:
#        while (ser.in_waiting>0):
#            print("in: "+str(ser.in_waiting))
#            ser.reset_input_buffer()
#            time.sleep(.01)
#        while (ser.out_waiting>0):
#            print("out: "+str(ser.out_waiting))
#            ser.reset_output_buffer()
#            time.sleep(.01)
#        ser.write(message.encode())
#        print("message sent")
#        data = ser.readline()
#        if data or True:
#            print(data.decode())
#        else:
#            print('nothing')

    #AirQualitySensor
    aQS = random.random()
    #AmbientTempSensor
    aTS = random.random()
    #GasContentSensor
    gCS = random.random()
    #ObjectTempSensor
    oTS = random.random()


    print('Sending this data to the subscriber')
    sensorData= "aQS: %.2f, aTS: %.2f, gCS: %.2f, oTS: %.2f" % (aQS,aTS,gCS,oTS)
    time.sleep(1)
    status = cliePub.publishInfo(sensorData)
    print(sensorData)
    #tracker += 1
    #print('At ' + str(tracker) + ' second ' + str(status))
    #newData = cliePub.parseGuiData(sensorData)
    #print('Data parsed into dictionary')
    #print(newData)
    #print('\n')

cliePub.foreverLoopClient()


#cliePub.stopPublishLoop()
