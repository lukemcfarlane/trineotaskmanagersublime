 # 
 # @author  Luke
 # @date    Feb 2014
import sublime, sublime_plugin, os.path, os, re, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import requests

class TaskManagerService(object):
    def __init__(self, settings):
        self.sessionId = settings.get("sessionId")
        self.userId = settings.get("userId")
        self.baseUrl = settings.get("baseUrl")

    def checkConnection(self):
        print("Checking connection with sid: " + self.sessionId)
        resource = "sobjects"
        headers = { "Authorization": "Bearer " + self.sessionId }
        res = requests.get(self.baseUrl + resource, headers=headers)
        print("Status code: " + str(res.status_code))
        print("Response body: " + res.text)
        return res.status_code == requests.codes.ok

    def getCurrentTime(self):
        print("Performing query to get current time: " + self.sessionId)
        resource = "query"
        queryStr = "SELECT Id, Is_Stopwatch_running__c, Stopwatch_Start_Time__c, Project_Entered__c, Description_Entered__c, Accumulated_Time_Seconds__c, Accumulated_Time__c, Accumulated_Time_Hours__c FROM TaskManager_Session_Data__c WHERE SetupOwnerId = '" + self.userId + "'"
        headers = { "Authorization": "Bearer " + self.sessionId }
        res = requests.get(self.baseUrl + resource + "/?q=" + queryStr, headers=headers)
        print("Status code: " + str(res.status_code))
        print("Response body: " + res.text)
        if res.status_code == requests.codes.ok:
            currentTime = json.loads(res.text)
            return currentTime["records"][0]
        else:
            sublime.message_dialog("Oops, that didn't quite go to plan. We got an error response code '" + str(res.status_code) + "'")
