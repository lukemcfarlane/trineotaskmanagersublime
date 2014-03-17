Trineo Task Manager
=======================
A Sublime Text 3 plugin.
-------------------------

Manage time logging from with Sublime Text 3.

Currently supported commands:
- Connecting to Salesforce by entering current session ID (can use included bookmarklet to get session ID from Salesforce in your browser)
- View current timer


Installation
------------

Copy the following files into a new folder "TrineoTaskManager" inside your Sublime Packages directory:
- TrineoTaskManagerSublime.py
- task_manager.py
- Default.sublime-commands
- TrineoTaskManager.sublime-settings
- Main.sublime-menu
- requests (directory)

Get your Salesforce session ID:
- Create a new bookmark called "Get Session ID" in your browser with the bookmarklet code in GetSessionId.bookmarklet
- Login and go to your Salesforce "Home" tab (important)
- Click the bookmarklet, your current session ID should be preselected in the dialog that pops up so that you can easily copy/paste into Sublime Text 3

**Note:** to locate your Sublime Packages directory, from within Sublime Text go to the Sublime Text menu -> Preferences -> Browse Packages.

