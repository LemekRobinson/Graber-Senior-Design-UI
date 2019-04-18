import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import pdb

class clientObjClass(object):

    global on_connect
    global on_subscribe
    global on_message
    global on_publish
    global on_log

    def __init__(self):
        self.__broker = ''
        self.__port = 0
        self.__topic = ''
        self.__client = ''

    def createClient(self):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_subscribe = on_subscribe
        client.on_publish = on_publish
        #client.on_log = on_log
        self.__client = client
        #return client

    def setClientParams(self,broker,port,topic):
        self.__broker = broker
        self.__port = port
        self.__topic = topic

    def getClientParams(self):
        params = dict()
        params['broker'] = self.__broker
        params['port'] = self.__port
        params['topic'] = self.__topic
        return params

    def connectClient(self):
        self.__client.connect(self.__broker,self.__port,60)

    def disconnectClient(self):
        self.__client.disconnect()

    def getClient(self):
        return(self.__client)

    def on_connect(client, userdata, flags, rc):
        print("rc: " + str(rc))

    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        #return(str(msg.payload))

    def on_publish(client, obj, mid):
        print("mid: " + str(mid))
        pass

    def publishData(self,data):
        #pdb.setTrace()
        #print('got To Publish in clieObj')
        self.__client.publish(self.__topic,data)
        return('I published to the topic: [' + str(self.__topic) + '] with this data: [' + str(data) +']')

    def on_subscribe(client, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def subscribeToTopic(self):
        self.__client.subscribe(self.__topic)

    def printFromSubscriber(self):
        subTestClient = self.getClient()
        print('Got into print from subscriber')
        #subTestClient.on_message()

        print('Subscribed simply')
        subData = subscribe.simple(self.__topic,hostname = self.__broker,port = self.__port)
        #print("%s %s" % (str(subData.topic), str(subData.payload)))
        return(subData)

    def on_log(client, obj, level, string):
        print(string)

    def loopClientForever(self):
        self.__client.loop_forever()

    def startLoop(self,indicator):
        if indicator.__eq__('f'):
            self.__client.loop_forever()
            str = 'Successful loop (forever) start'
        else:
            self.__client.loop_start()
            str = 'Successful loop start'
        return(str)

    def endLoop(self):
        self._client.loop_stop()
        str = 'Successful loop end'
        return(str)
