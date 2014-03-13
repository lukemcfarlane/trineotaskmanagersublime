 # 
 # @author  Luke
 # @date    Feb 2014
import sublime, sublime_plugin, os.path, os, re, sys
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
            if self.sessionId == "":
                if sublime.ok_cancel_dialog("Uh oh, your Salesforce session ID has not been set, would you like to set it now?"):
                    self.window.run_command("connect_to_salesforce")
            else:
                # self.window.active_view().set_status("z_current_timer", "(timer will show here)")
                if self.checkConnection(self.sessionId):
                    sublime.status_message("(timer will show here)")
                else:
                    if sublime.ok_cancel_dialog("Uh oh, we tried pinging Salesforce and your session ID seems to be expired or invalid. Would you like to update it?"):
                        self.window.run_command("connect_to_salesforce")


    def checkConnection(self, sessionId):
        print("Checking connection with sid: " + sessionId)
        baseUrl = "https://trineo.my.salesforce.com/services/data/v29.0/"
        resource = "sobjects"
        headers = { "Authorization": "Bearer" + sessionId }
        res = requests.get(baseUrl + resource, headers=headers)
        print("Status code: " + str(res.status_code))
        print("Response body: " + res.text)
        return res.status_code == requests.codes.ok






