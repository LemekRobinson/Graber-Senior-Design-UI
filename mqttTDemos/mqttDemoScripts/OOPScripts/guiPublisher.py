import clientObjClass as cli
import pdb


class guiPublisher(object):

    def __init__(self):
        self.__connectionStatus = False
        clientObj = cli.clientObjClass()
        self.__clientObj = clientObj

    def getClient(self):
        a = self.__clientObj.getClient()
        return(a)

    def buildPublisher(self):
        self.__clientObj.createClient()

    def addPublisherParams(self,broker,port,topic):
        self.__clientObj.setClientParams(broker,port,topic)

    def connectPublisher(self):
        self.__clientObj.connectClient()
        self.__connectionStatus = True

    def startPublishLoop(self,indicator):
        self.__clientObj.subscribeToTopic()
        status = self.__clientObj.startLoop(indicator)

    def stopPublishLoop(self):
        status = self.__clientObj.endLoop()

    def publishInfo(self,data):
        a = self.__clientObj.publishData(data)
        return(a)

    def checkConnection(self):
        return(self.__connectionStatus)

    def checkClientDetails(self):
        details = self.__clientObj.getClientParams()
        return(details)
