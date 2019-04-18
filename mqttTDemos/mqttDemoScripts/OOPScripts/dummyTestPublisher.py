import clientObjClass as cli
import guiPublisher as guiPub
import pdb
import time

broker = '143.215.81.180'
port = 1883
topic = 'dummyTest'
tracker = 0

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

while (tracker < 45):
    status = cliePub.publishInfo('testMsg')
    tracker += 1
    time.sleep(1)
    print('At ' + str(tracker) + ' second ' + str(status))


cliePub.startPublishLoop('f')


#cliePub.stopPublishLoop()
