import clientObjClass as cli
import pdb


class guiSubscriber(object):

    def __init__(self):
        self.__connectionStatus = False
        clientObj = cli.clientObjClass()
        self.__clientObj = clientObj
        self.__guiDataPreParse = ''
        self.__sensorDataPostParse = {'AirQualitySensor': '', 'AmbientTempSensor' : '', 'GasContentSensor' : '','ObjectTempSensor':''}


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


    def receiveGuiData(self):
        subscribedData = self.__clientObj.printFromSubscriber()
        print('subscribed Data')
        self.__sensorDataPreParse = subscribedData.payload
        return(self.__sensorDataPreParse)

    def foreverLoopClient(self):
        self.__clientObj.loopClientForever()

    def startSubscribeLoop(self,indicator):
        self.__clientObj.startLoop(indicator)

    def stopSubscribeLoop(self):
        self.__clientObj.endLoop()

    def isFloat(self,string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def parseGuiData(self,data):
        self.__sensorDataPreParse = data
        data = str(data) #Casting to string type due to error between python 2 and 3
        sensorList = data.split(",")

        if 'aQS' in sensorList[0] or 'aTS' in sensorList[1] or 'gCS' in sensorList[2] or 'oTS' in sensorList[3] :

            aQSFloat = sensorList[0]
            aQSFloatData = aQSFloat.split(":")
            aQSFloatData[1] = float(aQSFloatData[1])
            print(self.isFloat(aQSFloatData[1]))
            self.__sensorDataPostParse['AirQualitySensor'] = aQSFloatData[1]

            aTSFloat = sensorList[1]
            aTSFloatData = aTSFloat.split(":")
            aTSFloatData[1] = float(aTSFloatData[1])
            print(self.isFloat(aTSFloatData[1]))
            self.__sensorDataPostParse['AmbientTempSensor'] = aTSFloatData[1]

            gCSFloat = sensorList[2]
            gCSFloatData = gCSFloat.split(":")
            gCSFloatData[1] = float(gCSFloatData[1])
            print(self.isFloat(gCSFloatData[1]))
            self.__sensorDataPostParse['GasContentSensor'] = gCSFloatData[1]

            oTSFloat = sensorList[3]
            oTSFloatData = oTSFloat.split(":")
            oTSFloatData[1] = float(oTSFloatData[1])
            print(self.isFloat(oTSFloatData[1]))
            self.__sensorDataPostParse['ObjectTempSensor'] = oTSFloatData[1]

        return(self.__sensorDataPostParse)

    def checkConnection(self):
        return(self.__connectionStatus)

    def checkClientDetails(self):
        details = self.__clientObj.getClientParams()
        return(details)
