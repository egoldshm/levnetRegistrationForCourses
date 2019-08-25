import json
import requests

import threading
import time

from tools import *

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


headers = {'Host' : 'levnet.jct.ac.il', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}

loginUrl = 'https://levnet.jct.ac.il/api/home/login.ashx?action=TryLogin'
ScheduleStart = 'https://levnet.jct.ac.il/Student/Schedule/Start.aspx'
BuildScheduleStart = 'https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=LoadDataForBuildScheduleStart'
SelectSemesterForBuildSchedule = 'https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=SelectSemesterForBuildSchedule'
CoursesNew = 'https://levnet.jct.ac.il/Student/Schedule/CoursesScheduleNew.aspx'
CoursesScheduleNew = 'https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=LoadData'
LoadCoursesForTrack = 'https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=LoadCoursesForTrack'
LoadCoursesForProgram = 'https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=LoadCoursesForProgram'
SaveGroupsSelection = 'https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=SaveGroupsSelection'
LoadRegWarnings = 'https://levnet.jct.ac.il/api/student/RegWarningsForCourses.ashx?action=LoadRegWarnings'

def loginToLevnet(username, password):
    '''function that try to login to levnet.jct.ac.il
if success -> return the session, if fail -> return False'''
    with requests.Session() as session:
        r = session.post(loginUrl, data = {'username' : username, 'password' : password }, headers = headers)
        return session if toJson(r)["success"] else False    

def addCourse(username, password, courseId, groupNumbers):
        s = loginToLevnet(username, password)
        if s == False:
            return "שם משתמש או סיסמה שגויים"

        time = checkIfIsOpen(s, username, password)
        if time == False:
            return "המערכת אינה פתוחה עדיין"
        
        
        POST(s, SelectSemesterForBuildSchedule, data = time)
        
        GET(s, CoursesNew)
        
        r = POST(s, CoursesScheduleNew, data = { 'username' : username, 'password' : password })
        tracks = toJson(r)["tracks"]
        for i in tracks:
            r = POST(s, LoadCoursesForTrack, data = {"selectedTrack": i["id"]})
        
            id = getIdOfCourse(r,courseId)
            if id == -1:
                continue

            r = POST(s, LoadCoursesForProgram, data = {"programMemberId":id})

            idOfGroups = getIdOfGroups(r,groupNumbers)
            if idOfGroups == -1:
                continue
            

            print(f"Register to: {idOfGroups}")#Until Now - Work fine.
        
            POST(s, SaveGroupsSelection, data = idOfGroups)#problem here        
            return "Done"

        return "Not Found"



def checkIfIsOpen(s, username, password):
    '''check if schedule is open. if open -> return semester and year that open. if not -> return false.'''
    GET(s, ScheduleStart)
    r = POST(s, BuildScheduleStart, data = { 'username' : username, 'password' : password })
    whatOpen = toJson(r)["semestersScheduleCreation"]
    if whatOpen == []:
        return False
        
    year = whatOpen[0]["academicYearId"]
    semester = whatOpen[0]["semesterId"]
    return {"academicYear":year,"semester":semester}


def getFinishData(s):
    ''' return טופס הערות לקורסים'''
    r = POST(s, LoadRegWarnings, data = '')
    return toJson(r)["regWarnings"]
        
        
if __name__ == '__main__':
    #הרשמה להסתברות
    print(addCourse('egoldshm', '058jabcc400', 120701, [1,11]))
