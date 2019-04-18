import paho.mqtt.client as mqtt


class Broadcaster(object):



    def __init__(self,broker,port,topic):
        self.__broker = broker
        self.__port = port
        self.__topic = topic

    def on_connect(client, obj, flags, rc):
        print("rc: " + str(rc))

    def on_message(client, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def on_subscribe(client,obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(client, obj, level, string):
        print(string)


    def main(self):

        client = mqtt.Client()
        client.connect(self.__broker,self.__port)
        client.subscribe(self.__topic)

        client.loop_forever()


if __name__ == "__main__":
    broker = '143.215.95.218'
    port = 1883
    topic = 'dummyTest'

    brdcst = Broadcaster(broker,port,topic)
    brdcst.main() #Runs main method
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
