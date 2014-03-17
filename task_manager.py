 # 
 # @author  Luke
 # @date    Feb 2014
import sublime, sublime_plugin, os.path, os, re, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import requests

class TaskManagerService(object):
    def __init__(self, settings):
        self.settings = settings

    def checkConnection(self):
        print("Checking connection with sid: " + self.settings.sessionId)
        resource = "sobjects"
        headers = { "Authorization": "Bearer " + self.settings.sessionId }
        res = requests.get(self.settings.baseUrl + resource, headers=headers)
        print("Status code: " + str(res.status_code))
        print("Response body: " + res.text)
        return res.status_code == requests.codes.ok

    def getCurrentTime(self):
        print("Performing query to get current time: " + self.settings.sessionId)
        resource = "query"
        queryStr = "SELECT Id, Is_Stopwatch_running__c, Stopwatch_Start_Time__c, Project_Entered__c, Description_Entered__c, Accumulated_Time_Seconds__c, Accumulated_Time__c, Accumulated_Time_Hours__c FROM TaskManager_Session_Data__c WHERE SetupOwnerId = '" + self.settings.userId + "'"
        headers = { "Authorization": "Bearer " + self.settings.sessionId }
        res = requests.get(self.settings.baseUrl + resource + "/?q=" + queryStr, headers=headers)
        print("Status code: " + str(res.status_code))
        print("Response body: " + res.text)
        if res.status_code == requests.codes.ok:
            currentTime = json.loads(res.text)["records"][0]
            print(currentTime)
            return currentTime
        else:
            sublime.message_dialog("Oops, that didn't quite go to plan. We got an error response code '" + str(res.status_code) + "'")


class Settings(object):
    def __init__(self):
        self.settings = sublime.load_settings("TrineoTaskManager.sublime-settings")
        self.sessionId = self.settings.get("sessionId")
        self.userId = self.settings.get("userId")
        self.baseUrl = self.settings.get("baseUrl")

    def validate(self):
        settingsValid = True 
        if self.settings is None:
           sublime.message_dialog("Failed to load plugin settings 'TrineoTaskManager.sublime-settings")
           settingsValid = False
        else:
            if self.sessionId == "":
                if sublime.ok_cancel_dialog("Uh oh, your Salesforce session ID has not been set, would you like to set it now?"):
                    self.window.run_command("connect_to_salesforce")
            if self.userId == "":
                sublime.message_dialog("Oops, we are going to need a Salesforce user ID to retrieve time data. You can set this by going to Sublime Text -> Preferences -> Package Settings -> Trineo Task Manager -> Settings - User.")
                settingsValid = False
            if self.baseUrl == "":
                sublime.message_dialog("Oops, we are going to need a base URL to retrieve time data via the API. You can set this by going to Sublime Text -> Preferences -> Package Settings -> Trineo Task Manager -> Settings - User.")
                settingsValid = False
        return settingsValid

    def set(self, name, newValue):
        self.settings.set(name, newValue);
        sublime.save_settings("TrineoTaskManager.sublime-settings")



