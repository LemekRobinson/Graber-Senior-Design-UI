import clientObjClass as cli
import guiSubscriber as guiSub

broker = '143.215.81.180'
port = 1883
topic = 'dummyTest'

clieSub = guiSub.guiSubscriber()

clieSub.buildSubscriber()
print
clieSub.addSubscriberParams(broker,port,topic)

clieSub.connectSubscriber()

a = clieSub.checkConnection()
b = clieSub.checkClientDetails()

print("Subscriber details")
print(b)
print("Subscriber is connected: ")
print(a)

subClient = clieSub.getClient()

print(subClient)

clieSub.startSubscribeLoop('f')
