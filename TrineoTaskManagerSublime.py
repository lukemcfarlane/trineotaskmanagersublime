 # 
 # @author  Luke
 # @date    Feb 2014
import sublime, sublime_plugin, os.path, os, re, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import requests, task_manager

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
        self.tm = task_manager.TaskManagerService(self.settings)
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
                if self.tm.checkConnection():
                    currentTime = self.tm.getCurrentTime()
                    timeStatusStr = str(currentTime["Project_Entered__c"]) + ": " + str(currentTime["Description_Entered__c"]) + ("" if currentTime["Is_Stopwatch_running__c"] else " (paused)")
                    sublime.status_message(timeStatusStr)
                else:
                    if sublime.ok_cancel_dialog("Uh oh, we tried pinging Salesforce and your session ID seems to be expired or invalid. Would you like to update it?"):
                        self.window.run_command("connect_to_salesforce")





