# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 15:40:11 2022

@author: zidda
"""

import os
from notion_client import Client
from pprint import pprint
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests, json

def window():
   app = QApplication(sys.argv)
   w = QWidget()
   b = QLabel(w)
   b.setText("List of Tasks")
   w.setGeometry(100,100,500,450)
   b.move(50,20)
   w.setWindowTitle("PyQt5")
   w.show()
   sys.exit(app.exec_())
   


notion = Client(auth="secret_UZep77jQV9Atnft7KMSUxgpJaYo7mynPBOBjAEhPBhS")
list_users_response = notion.users.list()
#pprint(list_users_response)

schoolWork = notion.databases.query(
    **{
        "database_id": "efb13db6cb8d4d338aa23f9eca04d38b",
    }
)

taskList = notion.databases.query(
    **{
        "database_id": "03c81a69ceb040368bc6afeab26a9c2b",
    }
)

#pprint(schoolWork)
schoolworkKeys = list(schoolWork.values())

incompleteTasks = []

for i in range(0, len(schoolworkKeys)+100):
    try:
        #print(schoolworkKeys[1][i].get("properties").get("Name").get("title")[0].get("text").get("content"))
        print(schoolworkKeys[1][i].get("properties").get("Status").get("status").get("name"))
        completeStatus = schoolworkKeys[1][i].get("properties").get("Status").get("status").get("name")
        if completeStatus == "Not started" or completeStatus == "In progress":
            incompleteTasks.append(completeStatus)
    except:
        pass
        #print("task not found") https://www.notion.so/ziddane-isahaku/03c81a69ceb040368bc6afeab26a9c2b?v=5405b26441d74a19871f68ac66dc3976
#print(schoolworkKeys[1])#[len(schoolworkKeys[1])-2].get("properties").get("Length of Task").get("number"))
#https://www.notion.so/ziddane-isahaku/d0dba3193f2242b294070cfffb8f22cd?pvs=4
print(incompleteTasks)


headers = {
    "Authorization": "Bearer " + "secret_UZep77jQV9Atnft7KMSUxgpJaYo7mynPBOBjAEhPBhS",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def updatePage(headers, nthTask, percentToday):
    updateUrl = "https://api.notion.com/v1/pages/d0dba3193f2242b294070cfffb8f22cd"

    updateData = {
        "properties": {
            "Nth task": {
                "number": nthTask
            },
            "Finish X Percent Today": {
                "number": percentToday
            },
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": "wacky"
                        }
                    }
                ]
            }
        }
    }

    data = json.dumps(updateData)

    response = requests.request("PATCH", updateUrl, headers=headers, data=data)
    print(taskList.values())
    #print(response.status_code)
    #print(response.text)
    
updatePage(headers, 5, 50)

"""
{'object': 'page', 
 'id': 'fb4fb0a6-af39-4850-9b63-25ee9fbaff20', 
 created_time': '2023-04-27T19:42:00.000Z', 
 'last_edited_time': '2023-04-27T19:42:00.000Z', 
 'created_by': {'object': 'user', 'id': '5be80a0f-38b0-4c72-9e42-c7f134e3afec'}, 
 'last_edited_by': {'object': 'user', 'id': '5be80a0f-38b0-4c72-9e42-c7f134e3afec'}, 
 'cover': None, 
 'icon': None, 
 'parent': {'type': 'database_id', 'database_id': 'efb13db6-cb8d-4d33-8aa2-3f9eca04d38b'}, 
 'archived': False, 
 'properties': {
     'Course': {
         'id': 'FROV', 
         'type': 'relation', 
         'relation': [{'id': 'bbf103ea-d88b-447b-ad79-dbb08b462c42'}], 
         'has_more': False
         }, 
     'Status': {
         'id': 'HReV', 
         'type': 'status', 
         'status': {
             'id': '38170805-12ad-4137-a2a2-1bbe445d552f', 
             'name': 'Done', 
             'color': 'green'}}, 
     'Type': {
         'id': 'K%5ETT', 
         'type': 'select', 
         'select': None}, 
     'Due date': {
         'id': 'w%5B%3EF', 
         'type': 'date', 
         'date': None}, 
     'Name': {
         'id': 'title', 
         'type': 'title', 
         'title': [{
             'type': 'text', 
             'text': {'content': '10.1 Intro to Limits HW', 'link': None}, 
             'annotations': {
                 'bold': False, 
                 'italic': False, 
                 'strikethrough': False, 
                 'underline': False, 
                 'code': False, 
                 'color': 'default'}, 
             'plain_text': '10.1 Intro to Limits HW', 'href': None}]}}, 
 'url': 'https://www.notion.so/10-1-Intro-to-Limits-HW-fb4fb0a6af3948509b6325ee9fbaff20'}

"""

#if __name__ == '__main__':
 #  window()





