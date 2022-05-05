from __future__ import print_function
from mimetypes import init
import mimetypes
from tkinter import N
from unicodedata import name

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaIoBaseDownload

import io
import os
import shutil
import sys

import subprocess



SCOPES = ['https://www.googleapis.com/auth/drive.readonly.metadata', 'https://www.googleapis.com/auth/drive.appdata', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive']
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))


customers = ['techstar', 'houston_plastics']
answers = ['y', 'n']

def list_folders():
    global file_list
    file_list = []
    global file_id
    file_id = []
    global full_id
    files = DRIVE.files().list().execute().get('files', ['id'])
    for item in files:
        if str(item['mimeType']) == str('application/vnd.google-apps.folder'):
            file_list += (item['name'],)
            file_id += (item['id'],)
    print("Folders in google drive ")
    print("------------------------")
    print(file_list)
    print("------------------------")
    global folder_name
    folder_name = input("Choose folder to download \n")
    if not folder_name in file_list: 
        while (not folder_name in file_list):
            folder_name = input("Invalid folder name, please type folder name exactly as listed. \n")
    

def get_id():
    list_folders()
    index = file_list.index(folder_name)
    full_id = file_id[index]
    image_list = DRIVE.files().list(q =f"'{full_id}' in parents").execute().get('files', 'id')
    global image_id
    image_id = []
    for file in image_list:
       image_id += (file['id'],)

    

def download_images():
    get_id()
        
    print("Downloading " + str(len(image_id)) + " images")
    image_names = []
    i = 0
    while i < (len(image_id)):
        request = DRIVE.files().get_media(fileId= image_id[i],)
        fh = io.FileIO(f'img_{i}.jpg', 'wb')
        image_names.append(f'img_{i}')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))
        i += 1
    customers = ['techstar', 'houston_plastics']
    print("------------------------")
    customer = input(f"Where to place images?\n------------------------\n{customers}\n------------------------\nType in a customer name from list \n").lower().replace(" ", "_")
    while (not customer in customers):
        customer = input("Invalid answer, type in a customer name. \n").lower().replace(" ", "_")
    print("------------------------")
    path = f'I:GTMT/{customer}'
    destination = os.listdir(f'{path}')
    print(destination)
    print("------------------------")
    location = input("Choose a folder to move images to\n").lower().replace(" ", "_")
    while (not location in destination):
        location = input("Invalid answer, type in a folder name. \n").lower().replace(" ", "_")
    path = os.path.join(path, location, "images")

    k = 0
    while k < len(image_names): 
        try:
            shutil.copy(f'C:/Python Scripts/new_job/{image_names[k]}.jpg', path)
        except:
            print("Error while moving files, files already exist ")
            query = input("Overwrite files? y/n\n")
            if not query in answers:
                while (not query in answers):
                    query = input("Invalid answer please type 'y' or 'n'\n")
            if query == 'y':
                shutil.move(f'C:/Python Scripts/new_job/{image_names[k]}.jpg', path)
        try:
            os.remove(f'{image_names[k]}.jpg')
        except:
            print("Error while deleting file ", image_names[k])
        k += 1

    print('Images moved to new folder \n')    
    input('Press Enter To Exit... ')
    


def create_new_mold():
    customers = ['techstar', 'houston_plastics']
    customer = input(f'---------------------\n{customers}\n---------------------\n Type in a customer name from list \n').lower().replace(" ", "_")
    while (not customer in customers):
        customer = input("Invalid answer, type in a customer name. \n").lower().replace(" ", "_")
    new_mold = input("Input new mold name: \n").lower().replace(" ", "_")
    
    path = f'I:GTMT/{customer}'
    new_path = os.path.join(path, new_mold)
    already_exists = os.path.isdir(new_path)
    if (already_exists == False):
        os.mkdir(new_path)
        new_path = os.path.join(new_path, 'images')
        os.mkdir(new_path)
    elif already_exists:
        query = input("Folder already exists overwrite? y/n\n")
        if not query in answers:
            while (not query in answers):
                query = input("Invalid answer please type 'y' or 'n'\n")
        if query == 'y':
            shutil.rmtree(new_path, ignore_errors=True)
            os.mkdir(new_path)
    
            new_path = os.path.join(new_path, 'images')
    
            os.mkdir(new_path)
    print("Directory set up for new mold.\n")
    image_query = input("Would you like to download mold images to folders? y/n\n")
    if not image_query in answers:
        while (not image_query in answers):
            image_query = input("Invalid answer please type 'y' or 'n'\n")
    elif image_query == 'y':
        download_images()
    else:
         input('Press Enter To Exit... ')

def help():
    print("-nm\n-dmi\n-quit")
    
commands = ['-nm', '-dmi', '-help', '-quit', '-gi']
help_commands =['-nm', '-dmi', '-quit']

print("Welcome what would you like to do? \n")
print("Options \n-----------------")
print("type -nm to create folders for a new mold ")
print("type -dmi to download mold images ")
print("type -quit to close program ")
command = input("type -help to see available commands again \n")

#change to switch statement
if not command in commands:
    while (not command in commands):
        command = input("Invalid command, type -help for commands. \n")
if command == '-help':
    help()
    while (not command in help_commands):
        command = input("")
if command == '-nm':
    create_new_mold()
if command == '-quit':
    sys.exit()
if command == '-dmi':
    download_images()
