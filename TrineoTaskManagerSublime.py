 # 
 # @author  Luke
 # @date    Feb 2014
import sublime, sublime_plugin, os.path, os, re, sys

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
                sublime.status_message("(timer will show here)")



