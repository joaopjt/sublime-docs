import threading
import os
import json

import sublime
import sublime_plugin

PACKAGES = []

class DocsCommand(sublime_plugin.WindowCommand):
  def getPackages(path):
    packages = []
    
    with open(path + '/package.json', 'r', 'utf-8') as packageFile:
      print(packageFile.read())
      data = json.loads(packageFile.read())

      if data.get('devDependencies'):
        for package, version in data['devDependencies']:
          packages.append(package)

      if data.get('dependencies'):
        for package, version in data['dependencies']:
          packages.append(package)

    return packages

  def getConfigPath(self):
    with open(self.window.folders()[0] + '/docs.json', 'r') as config:
      print(config.read())
      data = json.loads(config.read())
    return data['base_path'] | self.window.folders()[0]

  def display_list(self, packages):
    self.packages = packages

    self.window.show_quick_panel(packages, self.on_done)

  def on_done(self, index):
    self.window.open_file(self.window.folders()[0] + '/node_modules/' + PACKAGES[index] + '/README.md')

  def run(self):
    global PACKAGES
    basePath = self.getConfigPath()
    print(basePath)
    PACKAGES = DocsCommand.getPackages(basePath)
    self.display_list(PACKAGES)