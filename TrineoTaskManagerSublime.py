 # 
 # @author  Luke
 # @date    Feb 2014
import sublime, sublime_plugin, os.path, os, re, sys

class ConnectToSalesforceCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window = self.window
        self.window.show_input_panel('Current Salesforce session ID', '', self.setSessionId, None, None)

    def setSessionId(self, id):
        self.id = id
        # print("Salesforce session ID saved")

