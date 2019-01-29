import threading
import os
import json

import sublime
import sublime_plugin

PACKAGES = []
BASEPATH = '/'

class DocsCommand(sublime_plugin.WindowCommand):
  def verifyOpenedFolder(self):
    if not self.window.folders():
      sublime.message_dialog('No project folder opened.')
      return False

    return True

  def getConfigPath(self):
    try:
      with open(self.window.folders()[0] + '\\.docsconfig', 'r') as config:
        data = config.read()
      data = json.loads(data)
      data = data['base_path']
    except:
      data = '/'

    return data

  def getPackages(self):
    packages = []
    try:
      with open(self.window.folders()[0] + BASEPATH + 'package.json', 'r') as packageFile:
        data = packageFile.read()
    except:
      sublime.message_dialog('Unable to find the \'package.json\' file.')
      return

    data = json.loads(data)

    if data.get('devDependencies'):
      for package in data['devDependencies']:
        packages.append(package)

    if data.get('dependencies'):
      for package in data['dependencies']:
        packages.append(package)

    return packages

  def display_list(self, packages):
    self.packages = packages

    self.window.show_quick_panel(packages, self.on_done)

  def on_done(self, index):
    path = self.window.folders()[0] + BASEPATH + 'node_modules/' + PACKAGES[index] + '/README.md'

    if index == -1:
      return

    if os.path.exists(path):
      self.window.open_file(path)
    else:
      sublime.message_dialog('README from \'' + PACKAGES[index] + '\' not found.')

  def run(self):
    global PACKAGES
    global BASEPATH

    if self.verifyOpenedFolder():
      BASEPATH = self.getConfigPath()
      PACKAGES = self.getPackages()

      self.display_list(PACKAGES)