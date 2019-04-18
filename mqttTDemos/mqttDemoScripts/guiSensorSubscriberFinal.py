import clientObjClass as cli
import guiSubscriber as guiSub

broker = '143.215.99.102'
port = 1883
topic = 'guiParseTest'

clieSub = guiSub.guiSubscriber()

clieSub.buildSubscriber()

clieSub.addSubscriberParams(broker,port,topic)

clieSub.connectSubscriber()

a = clieSub.checkConnection()
b = clieSub.checkClientDetails()

#print("Subscriber details")
print(b)
#print("Subscriber is connected: ")
print(a)

subClient = clieSub.getClient()

print(subClient)
print('Here in the subscriber')

while True:
    print('Data received')
    sensorData = clieSub.receiveGuiData()
    print('Output from receive Gui Data')
    print(sensorData)
    #tracker += 1
    #print('At ' + str(tracker) + ' second ' + str(status))
    newData = clieSub.parseGuiData(sensorData)
    print('Data parsed into dictionary')
    print(newData)
    print('\n')

clieSub.foreverLoopClient()
