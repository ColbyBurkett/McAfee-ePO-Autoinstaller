from datetime import datetime
import getpass
import json
import mcafee
import os
import sys
import time
import yaml
   
print 'This script will Install Extensions, Check-in Packages, and Import Clients Tasks and Policies\n'
# Prompt for ePO v4.6+ IP
ePOIP=''
while ePOIP == '':
      ePOIP=raw_input('Please enter IP of McAfee ePO Server: ')

# Prompt for ePO username
ePOUser=''
while ePOUser == '':
      ePOUser=raw_input('Username: ')

# Prompt for ePO user's password
ePOUserPwd=''
while ePOUserPwd == '':
      ePOUserPwd=getpass.getpass('Password: ')

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

mc = mcafee.client(ePOIP, '8443', ePOUser, ePOUserPwd)
currentPath = os.getcwd()

# Create extensions, policies, and tasks by Group and Order, and Check-in any Packages
extensions=[]
packages=[]
policies=[]
tasks=[]
for key, value in data.items():
    for key2, value2 in value.items():
        for item in value2:
            if item['Type'] == 'Extension':
                extensions.append(item)
            elif item['Type'] == 'Package':
                packages.append(item)
            elif item['Type'] == 'Policy':
                policies.append(item)
            elif item['Type'] == 'Task':
                tasks.append(item)
extorder=(sorted(extensions, key = lambda i: (i['Order'])))
for extension in extorder:
      try:
            print("Installing extension: \r\n"+extension['Filename'])
            fileName='file:///'+extension['Filename']
            mc.ext.install(fileName)
      except:
            try:
                  print("Extension already exists. Upgrading extension: \r\n"+extension['Filename'])
                  fileName='file:///'+extension['Filename']
                  mc.ext.upgrade(fileName)
            except:
                  print("Extension already at expected level")
for package in packages:
    fileName = currentPath + '\\' + package['Filename']
    print("Checking in package: "+package['Filename'])
    mc.repository.checkInPackage(fileName,branch='Current',allowUpgrade=True)
for policy in policies:
    fileName = currentPath + '\\' + policy['Filename']
    print("Importing Policies: "+str(policy['Filename']))
    mc.policy.importPolicy(fileName)
for task in tasks:
    fileName = currentPath + '\\' + task['Filename']
    print("Importing Tasks: "+str(task['Filename']))
    mc.clienttask.importClientTask(fileName)
