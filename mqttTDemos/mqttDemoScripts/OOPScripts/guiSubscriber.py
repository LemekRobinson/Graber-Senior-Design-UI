import clientObjClass as cli
import pdb


class guiSubscriber(object):

    def __init__(self):
        self.__connectionStatus = False
        clientObj = cli.clientObjClass()
        self.__clientObj = clientObj

    def getClient(self):
        a = self.__clientObj.getClient()
        return(a)

    def buildSubscriber(self):
        self.__clientObj.createClient()

    def addSubscriberParams(self,broker,port,topic):
        self.__clientObj.setClientParams(broker,port,topic)

    def connectSubscriber(self):
        self.__clientObj.connectClient()
        self.__connectionStatus = True

    def startSubscribeLoop(self,indicator):
        self.__clientObj.startLoop(indicator)

    def stopSubscribeLoop(self):
        self.__clientObj.endLoop()

    def checkConnection(self):
        return(self.__connectionStatus)

    def checkClientDetails(self):
        details = self.__clientObj.getClientParams()
        return(details)
