import paho.mqtt.client as mqtt
import random
import clientObject as clientSub

class Subscriber(object):

    def __init__(self,client):
        self.__client = client

    def setData(self,data):
        self.__data = data

    def getData(self):
        return self.__data

    def parser(self,data):
        self.getData()

    def main(self,client):

        for i in range(0,400):
            #AirQualitySensor
            aQS = random.random()
            #InfraredTempSensor
            iRS = random.random()
            #GasContentSensor
            gCS = random.random()
            sensorData= 'aQS: %.2f, iRS: %.2f, gCS: %.2f' %(aQS,iRS,gCS)
            client.publish(self.topic,data)

        client.loop_forever()

if __name__ == "__main__":

    #Initializion Info
    broker = '10.0.0.245'
    port = 1883
    topic = 'pcTester'

    sbscrbr = Subscriber(broker,port,topic)
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client = mqtt.Client()

    client.connect(self.broker, self.port)

    sbscrbr.main(client) #Runs main method
