import json
import requests

import threading
import time

import Levnet
from URL import *

###############################################################
###                                                         ###
###                                                         ###
### This Code Written By Ariel Darshan And Eytan Goldshmidt ###
###                                                         ###
###             All rights reserved (C)                     ###
###                                                         ###
###                                                         ###
###############################################################


#proxy = 'https://localhost:8080'

def addCourse(username, password, courseId, groupNumbers):
    with Levnet.Session(username, password) as s:
        if s.Login() == False:
            return "שם משתמש או סיסמה שגויים"

        time = s.OpenSchedule()
        if time == False:
            return "המערכת אינה פתוחה עדיין"
        
        
        s.POST(SelectSemesterForBuildSchedule, json = time)
        
        s.GET(CoursesScheduleNew)
        
        tracks = s.LoadScheduleTracks()
        for track in tracks:
            r = s.POST(LoadCoursesForTrack, json = {"selectedTrack": track["id"]})
        
            ProgramId = getIdOfCourse(r,courseId)
            if id == -1:
                continue

            r = s.POST(LoadCoursesForProgram, json = {"programMemberId":ProgramId})

            idOfGroups = getIdOfGroups(r,groupNumbers)
            if idOfGroups == -1:
                continue
            

            print(f"Register to: {idOfGroups}")
        
            r = s.POST(SaveGroupsSelection, json = idOfGroups)    
            return "Done"

        return "Not Found"

def sendReportToUs(username, data):
    with requests.Session() as session:
        session.post("https://eitanbots.000webhostapp.com/levnet.php", verify=False, data = {"username": username, "meeting": str(data)})
"""
def getFinishData(s):
    ''' return טופס הערות לקורסים'''
    r = s.POST(LoadRegWarnings, data = '')
    return toJson(r)["regWarnings"]
        
"""

if __name__ == '__main__':
    #הרשמה להסתברות
    print(addCourse('egoldshm', "----------", 120701, [1,11]))
