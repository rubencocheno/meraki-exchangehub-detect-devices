from .api import Api

class Webex: 
    def __init__(self, botToken='', botRoom=''):
        self.baseUrl = "https://api.ciscospark.com/v1/"
        self.token = botToken
        self.room = botRoom

    def sendMessage(self, message):
        result =  Api.postRequest(self.baseUrl + 'messages', {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }, {
            "roomId": self.room,
            "markdown": message
        })
        return result