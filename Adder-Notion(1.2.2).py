# -*- coding: utf-8 -*-
"""
Created on Fri May 12 15:40:11 2023

@author: zidda
""" 

from notion_client import Client
import datetime as dt
import requests, json


#date = datetime.datetime.utcnow()
#utc_time = calendar.timegm(date.utctimetuple())
#print(utc_time)

notion = Client(auth="secret_UZep77jQV9Atnft7KMSUxgpJaYo7mynPBOBjAEhPBhS")
list_users_response = notion.users.list()
#pprint(list_users_response)

schoolWork = notion.databases.query(
    **{
        "database_id": "efb13db6cb8d4d338aa23f9eca04d38b",
    }
)

taskLists = notion.databases.query(
    **{
        "database_id": "03c81a69ceb040368bc6afeab26a9c2b",
    }
)

#pprint(schoolWork)
schoolworkKeys = list(schoolWork.values())

incompleteTaskKeys = []
taskList = []
taskWeights = []

for i in range(0, len(schoolworkKeys)+100):
    try:
        #print(schoolworkKeys[1][i].get("properties").get("Name").get("title")[0].get("text").get("content"))
        print(schoolworkKeys[1][i].get("properties").get("Status").get("status").get("name"))
        completeStatus = schoolworkKeys[1][i].get("properties").get("Status").get("status").get("name")
        if completeStatus == "Not started" or completeStatus == "In progress":
            incompleteTaskKeys.append(i)
            taskList.append(schoolworkKeys[1][i].get("properties"))
            taskWeights.append(0)
    except:
        pass
        #print("task not found") https://www.notion.so/ziddane-isahaku/03c81a69ceb040368bc6afeab26a9c2b?v=5405b26441d74a19871f68ac66dc3976
#print(schoolworkKeys[1])#[len(schoolworkKeys[1])-2].get("properties").get("Length of Task").get("number"))
#https://www.notion.so/ziddane-isahaku/d0dba3193f2242b294070cfffb8f22cd?pvs=4
print(incompleteTaskKeys)



headers = {
    "Authorization": "Bearer " + "secret_UZep77jQV9Atnft7KMSUxgpJaYo7mynPBOBjAEhPBhS",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def updatePage(headers, nthTask, percentToday, newTitle, url, percentComplete, status, date):
    updateUrl = url
    print(updateUrl)
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
                            "content": newTitle
                        }
                    }
                ]
            },
            "Percent Completed": {
                "number": percentComplete
            }, 
            "Status": {
                "multi_select": [
                        {
                            "name": status
                        }
                    ]
                },
            "Date": {
                "date": {
                    "start": date
                    }
                }
        }
    }

    data = json.dumps(updateData)

    response = requests.request("PATCH", updateUrl, headers=headers, data=data)
    #print(response.status_code)
    #print(response.text)
    
def updateName(headers, newTitle, url):
    updateUrl = url
    print(updateUrl)
    updateData = {
        "properties": {
            
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": newTitle
                        }
                    }
                ]
            }
        }
    }

    data = json.dumps(updateData)

    response = requests.request("PATCH", updateUrl, headers=headers, data=data)
    #print(response.status_code)
    #print(response.text)
print(taskList[0])


for i in range(0, len(taskWeights)):
    taskWeightSum = 0
    if taskList[i].get("Status").get("status").get("name") == "Not started":
        taskWeightSum += 50
    else: 
        taskWeightSum += 10 
    try:
        taskWeightSum += taskList[i].get("Importance").get("number") * 10
        taskWeightSum += taskList[i].get("Length of Task").get("number") * 10
        taskWeightSum += 100 - taskList[i].get("Completion %").get("number")
        
        #print(taskList[i])
        #print()
        date_1 = dt.date.fromisoformat((taskList[i].get("Due date").get("date").get("start")))
        date_2 = dt.date.today()
        d = date_1 - date_2 # datetime.timedelta(days=32)
        taskWeightSum += (14 - d.days)*12
        #print(d.days)
        #print()
    except:
        print()
    #daysTillDue = 
    #print(taskWeightSum)
    taskWeights[i] += taskWeightSum

for i in range(0, len(taskList)):
    taskList[i]["weight"] = taskWeights[i]
    #taskList[i]["date"] = taskWeights[i]

orderedList = sorted(taskList, key=lambda d: d['weight'], reverse = True) 
sortedWeights = sorted(taskWeights, reverse = True)
#l = (zip(taskWeights, taskList))
#importanceList = [taskWeightSum for _, taskWeightSum in sorted(zip(taskList, taskWeights))]
#taskWeights, taskList = zip(*sorted(zip(taskWeights, taskList)))
#taskWeights, taskList = (list(t) for t in zip(*sorted(zip(taskWeights, taskList))))
#for i in range(0, len(orderedList)):
    #print(orderedList[i].get("Name").get("title")[0].get("text")".get("conten"t"))
    
urlList = [
    "https://api.notion.com/v1/pages/d0dba3193f2242b294070cfffb8f22cd", 
    "https://api.notion.com/v1/pages/3df2f04fc7ca4c6aa9124aebde0849a2", 
    "https://api.notion.com/v1/pages/fd70e1484465465897a2a06f913fa62c", 
    "https://api.notion.com/v1/pages/36d21cce92ff44bb981fd79e509c96a6", 
    "https://api.notion.com/v1/pages/9f7c1be51ba5416c87126b8c6f365cdf", 
    "https://api.notion.com/v1/pages/df9b01ebedd44118b29b54973cfa68f5", 
    "https://api.notion.com/v1/pages/94a14c6750c341bdb0b51cbd74caed1d", 
    "https://api.notion.com/v1/pages/2a6d13ed4951452d8d73b5595ac798ce", 
    "https://api.notion.com/v1/pages/d82cfe0b02964d0ca5ff003adea806eb", 
    "https://api.notion.com/v1/pages/9f77b6a89af64950a1b06224e28a195d"
    ]

#https://www.notion.so/ziddane-isahaku/task-1-d0dba3193f2242b294070cfffb8f22cd?pvs=4
#https://www.notion.so/ziddane-isahaku/task-2-3df2f04fc7ca4c6aa9124aebde0849a2?pvs=4

#url0 = urlList[0]
#url1 = urlList[1]https://www.notion.so/ziddane-isahaku/task-3-fd70e1484465465897a2a06f913fa62c?pvs=4
#url2 = urlList[2]https://www.notion.so/ziddane-isahaku/task-3-fd70e1484465465897a2a06f913fa62c?pvs=4
#url3 = urlList[3]
#url4 = urlList[4]
#url5 = urlList[5]
##url6 = urlList[6]
#url7 = urlList[7]
#url8 = urlList[8]
#url9 = urlList[9]
"""
updatePage(headers, 5, 50, "wacky", "https://api.notion.com/v1/pages/d0dba3193f2242b294070cfffb8f22cd")
updatePage(headers, 5, 50, "wacky", "https://api.notion.com/v1/pages/3df2f04fc7ca4c6aa9124aebde0849a2")
updatePage(headers, 5, 50, "adsfg", "https://api.notion.com/v1/pages/fd70e1484465465897a2a06f913fa62c")
updatePage(headers, 5, 50, "wacky", "https://api.notion.com/v1/pages/36d21cce92ff44bb981fd79e509c96a6")
updatePage(headers, 5, 50, "wacky", "https://api.notion.com/v1/pages/9f7c1be51ba5416c87126b8c6f365cdf")
updatePage(headers, 5, 50, "wacky", "https://api.notion.com/v1/pages/df9b01ebedd44118b29b54973cfa68f5")
https://www.notion.so/ziddane-isahaku/Rough-Draft-d82cfe0b02964d0ca5ff003adea806eb?pvs=4
"""
def minLen(num, list1):
    if num < len(list1):
        return num
    else:
        return len(list1)

for i in range(0, minLen(10, orderedList)):
    #print(urlList[i])
    #updatePage(headers, 5, 50, "woah", urlList[i])
    
    
    newName = orderedList[i].get("Name").get("title")[0].get("text").get("content")
    if orderedList[i].get("Status").get("status").get("name") == "Done":
        newName = "awaiting task entry"
        
    percentCompleted = orderedList[i].get("Completion %").get("number")
    dueDate = orderedList[i].get("Due date").get("date").get("start")
    
    if percentCompleted == None:
        percentCompleted = 0
    date_1 = dt.date.fromisoformat((orderedList[i].get("Due date").get("date").get("start")))
    date_2 = dt.date.today()
    d = date_1 - date_2 # datetime.timedelta(days=32)
    if(d.days > 0):
        percentToComplete = (100 - percentCompleted) / d.days
    else:
        percentToComplete = (100 - percentCompleted);
    print(newName + ": " + str(percentToComplete))
    
    if percentToComplete < 0:
        newName = "awaiting entry"
        print("hello")
    
    dayToComplete = ""
    numToday = 0
    
    if d.days < 2 or (percentCompleted <= 10 and d.days < 5 and orderedList[i].get("Length of Task").get("number") > 4):
        dayToComplete = "Today"
        numToday += 1
    elif d.days >= 2:
        dayToComplete = "Tomorrow"
    elif d.days < 0 or percentCompleted == 100:
        dayToComplete = "Done 🙌"
    
    
    
    updatePage(headers, i, percentToComplete, newName, urlList[i], percentCompleted, dayToComplete, dueDate)
    
if numToday < 3:
    for i in range(0, minLen(10, orderedList)):
        #print(urlList[i])
        #updatePage(headers, 5, 50, "woah", urlList[i])
        
        
        newName = orderedList[i].get("Name").get("title")[0].get("text").get("content")
        if orderedList[i].get("Status").get("status").get("name") == "Done":
            newName = "awaiting task entry"
            
        percentCompleted = orderedList[i].get("Completion %").get("number")
        dueDate = orderedList[i].get("Due date").get("date").get("start")
        
        if percentCompleted == None:
            percentCompleted = 0
        date_1 = dt.date.fromisoformat((orderedList[i].get("Due date").get("date").get("start")))
        date_2 = dt.date.today()
        d = date_1 - date_2 # datetime.timedelta(days=32)
        if(d.days > 0):
            percentToComplete = (100 - percentCompleted) / d.days
        else:
            percentToComplete = (100 - percentCompleted);
        print(newName + ": " + str(percentToComplete))
        
        if percentToComplete < 0:
            newName = "awaiting entry"
            print("hello")
        
        dayToComplete = ""
        numToday = 0
        
        if d.days < 3 or (percentCompleted <= 25 and d.days < 5 and orderedList[i].get("Length of Task").get("number") > 4):
            dayToComplete = "Today"
            numToday += 1
        elif d.days >= 2:
            dayToComplete = "Tomorrow"
        elif d.days < 0 or percentCompleted == 100:
            dayToComplete = "Done 🙌"
        
        
        
        updatePage(headers, i, percentToComplete, newName, urlList[i], percentCompleted, dayToComplete, dueDate)
    
print("------------")

ITaskKeys = list(taskLists.values())

ITaskList = []

for i in range(0, len(ITaskKeys)+100):
    try:
            ITaskList.append(ITaskKeys[1][i])
    except:
        pass

#print(ITaskList)

for i in range(0, len(ITaskList)):
    print(ITaskList[i])
    print()
    try:
        #print(ITaskList[i].get("Percent Completed").get("number"))
        percent = int(ITaskList[i].get("properties").get("Percent Completed").get("number"))
        
        urlEnd = ITaskList[i].get("url")[-32:]
        
        if percent > 99.999:
            updateName(headers, "...", "https://api.notion.com/v1/pages/" + urlEnd)
    except:
        pass
