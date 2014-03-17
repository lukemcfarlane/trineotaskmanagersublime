 # 
 # @author  Luke
 # @date    Feb 2014
import sublime, sublime_plugin, os.path, os, re, sys, json
from imp import reload
sys.path.insert(0, os.path.dirname(__file__))
import requests, task_manager

class ConnectToSalesforceCommand(sublime_plugin.WindowCommand):
    def run(self):
        reload(task_manager)
        self.settings = task_manager.Settings() 
        if(self.settings.validate()):
            self.tm = task_manager.TaskManagerService(self.settings)
            self.window.show_input_panel('Current Salesforce session ID', '', self.setSessionId, None, None)

    def setSessionId(self, id):
        self.id = id
        self.settings.set("sessionId", self.id)
        print("Salesforce session ID saved")
        if not self.tm.checkConnection():
            if sublime.ok_cancel_dialog("Oops, that session Id would appear to be expired or invalid. Would you like to try entering it again?"):
                self.window.run_command("connect_to_salesforce")


class ShowCurrentTimeCommand(sublime_plugin.WindowCommand):
    def run(self):
        reload(task_manager)
        self.settings = task_manager.Settings() 
        self.view = self.window.active_view()
        if(self.settings.validate()):
            self.tm = task_manager.TaskManagerService(self.settings)
            if self.tm.checkConnection():
                currentTime = self.tm.getCurrentTime()
                hours = currentTime["Accumulated_Time_Hours__c"]
                minutes = currentTime["Accumulated_Time__c"]
                elapsedTimeStr = '%(hours)02d:%(minutes)02d' % \
                    { "hours": hours, "minutes": minutes }
                timeStatusStr = str(currentTime["Project_Entered__c"]) + ": " + str(currentTime["Description_Entered__c"]) + " [" + elapsedTimeStr + "]" + ("" if currentTime["Is_Stopwatch_running__c"] else " (paused)")
                self.view.set_status("z_tm_current_timer", timeStatusStr)
            else:
                if sublime.ok_cancel_dialog("Uh oh, we tried pinging Salesforce and your session ID seems to be expired or invalid. Would you like to update it?"):
                    self.window.run_command("connect_to_salesforce")

class StartNewTimerCommand(sublime_plugin.WindowCommand):
    def run(self):
        reload(task_manager)
        self.settings = task_manager.Settings() 
        self.view = self.window.active_view()
        if(self.settings.validate()):
            self.tm = task_manager.TaskManagerService(self.settings)
            if self.tm.checkConnection():
                availableProjects = self.tm.getAvailableProjects()
                self.projectNameArr = []
                self.projectIdArr = []
                for proj in availableProjects:
                    self.projectNameArr.append(proj["Name"])
                    self.projectIdArr.append(proj["Name"])
                self.window.show_quick_panel(self.projectNameArr, self.startTimer)
            else:
                if sublime.ok_cancel_dialog("Uh oh, we tried pinging Salesforce and your session ID seems to be expired or invalid. Would you like to update it?"):
                    self.window.run_command("connect_to_salesforce")


    def startTimer(self, selectedIndex):
        projectId = self.projectIdArr[selectedIndex]
        projectName = self.projectNameArr[selectedIndex]
        timeData = {
            "Project_Entered__c": projectName,
            "Description_Entered__c": "",
            "Is_Stopwatch_running__c": True,
            "SetupOwnerId": self.settings.userId
        }
        self.tm.saveTime(timeData)








