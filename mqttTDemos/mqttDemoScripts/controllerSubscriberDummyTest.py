import clientObjClass as cli
import controlSubscriber as controlSub

broker = '143.215.107.227'#This should be the IP address
#of the computer with GUI
port = 1883 #formerly 1883
topic = 'controllerTest'
serialPort = '/dev/ttyACM0'

clieSub = controlSub.controlSubscriber()

clieSub.buildSubscriber()

clieSub.addSubscriberParams(broker,port,topic)

clieSub.connectSubscriber()

clieSub.setSerialPort(serialPort)

a = clieSub.checkConnection()
b = clieSub.checkClientDetails()

print("Subscriber details")
print(b)
print("Subscriber is connected: ")
print(a)

controlSubClient = clieSub.getClient()

print(controlSubClient)
print('Here in the subscriber')
clieSub.connectToDUE()
while True:
    print('Output from receive Mvmnt')
    mvmntData = clieSub.receiveMvmnt()
    print('Data received')
    print(type(mvmntData))
    #tracker += 1
    #print('At ' + str(tracker) + ' second ' + str(status))

    newData = str(clieSub.writeToDUE(mvmntData))
    print('Data written to DUE')
    print(newData)
    print('\n')
    print("this is from the due"+newData)
clieSub.foreverLoopClient()
