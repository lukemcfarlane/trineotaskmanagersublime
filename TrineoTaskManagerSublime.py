 # 
 # @author  Luke
 # @date    Feb 2014
import sublime, sublime_plugin, os.path, os, re, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import requests

class ConnectToSalesforceCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.settings = sublime.load_settings("TrineoTaskManager.sublime-settings")
        self.window = self.window
        self.window.show_input_panel('Current Salesforce session ID', '', self.setSessionId, None, None)

    def setSessionId(self, id):
        self.id = id
        self.settings.set("sessionId", self.id)
        sublime.save_settings("TrineoTaskManager.sublime-settings")
        print("Salesforce session ID saved")


class ShowCurrentTimeCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.settings = sublime.load_settings("TrineoTaskManager.sublime-settings")
        if self.settings is not None:
            self.sessionId = self.settings.get("sessionId")
            self.userId = self.settings.get("userId")
            if self.sessionId == "":
                if sublime.ok_cancel_dialog("Uh oh, your Salesforce session ID has not been set, would you like to set it now?"):
                    self.window.run_command("connect_to_salesforce")
            elif self.userId == "":
                sublime.message_dialog("No user ID")
            else:
                # self.window.active_view().set_status("z_current_timer", "(timer will show here)")
                if self.checkConnection(self.sessionId):
                    currentTime = self.getCurrentTime(self.userId, self.sessionId)
                    timeStatusStr = str(currentTime["Project_Entered__c"]) + ": " + str(currentTime["Description_Entered__c"]) + ("" if currentTime["Is_Stopwatch_running__c"] else " (paused)")
                    sublime.status_message(timeStatusStr)
                else:
                    if sublime.ok_cancel_dialog("Uh oh, we tried pinging Salesforce and your session ID seems to be expired or invalid. Would you like to update it?"):
                        self.window.run_command("connect_to_salesforce")

    def getCurrentTime(self, userId, sessionId):
        # todo
        print("Performing query to get current time: " + sessionId)
        baseUrl = "https://trineo.my.salesforce.com/services/data/v29.0/"
        resource = "query"
        queryStr = "SELECT Id, Is_Stopwatch_running__c, Stopwatch_Start_Time__c, Project_Entered__c, Description_Entered__c, Accumulated_Time_Seconds__c, Accumulated_Time__c, Accumulated_Time_Hours__c FROM TaskManager_Session_Data__c WHERE SetupOwnerId = '" + userId + "'"
        headers = { "Authorization": "Bearer " + sessionId }
        res = requests.get(baseUrl + resource + "/?q=" + queryStr, headers=headers)
        print("Status code: " + str(res.status_code))
        print("Response body: " + res.text)
        if res.status_code == requests.codes.ok:
            currentTime = json.loads(res.text)
            return currentTime["records"][0]
        else:
            sublime.message_dialog("Oops, that didn't quite go to plan. We got an error response code '" + str(res.status_code) + "'")

    def checkConnection(self, sessionId):
        print("Checking connection with sid: " + sessionId)
        baseUrl = "https://trineo.my.salesforce.com/services/data/v29.0/"
        resource = "sobjects"
        headers = { "Authorization": "Bearer " + sessionId }
        res = requests.get(baseUrl + resource, headers=headers)
        print("Status code: " + str(res.status_code))
        print("Response body: " + res.text)
        return res.status_code == requests.codes.ok






