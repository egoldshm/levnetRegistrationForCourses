import json
import requests

import threading
import time

import Levnet

from tools import getIdOfCourse, getIdOfGroups


###############################################################
###                                                         ###
###                                                         ###
### This Code Written By Ariel Darshan And Eytan Goldshmidt ###
###                                                         ###
###               All rights reserved (C)                   ###
###                                                         ###
###                                                         ###
###############################################################


# proxy = 'https://localhost:8080'

def addCourse(username, password, courseId, groupNumbers, hasRimon):
    with Levnet.Session(username, password, not hasRimon) as s:
        if s.Login() == False:
            return "שם משתמש או סיסמה שגויים"

        time = s.OpenSchedule()
        if time == False:
            return "המערכת אינה פתוחה עדיין"

        s.SelectSemesterForSchedule(time)

        s.CoursesSchedule()

        tracks = s.LoadScheduleTracks()
        for track in tracks:
            r = s.LoadTrackCourses(track)

            ProgramId = getIdOfCourse(r, courseId)
            if ProgramId == -1:
                continue

            r = s.LoadProgramCourses(ProgramId)

            idOfGroups = getIdOfGroups(r, groupNumbers)
            if idOfGroups == -1:
                continue

            print(f"Register to: {idOfGroups}")

            s.SelectGroups(idOfGroups)
            return "Done"

        return "Not Found"


def sendReportToUs(*parms):
    try:
        if len(parms) % 2 != 0:
            parms = [""] + list(parms)
        d = {}
        for i in range(0, len(parms), 2):
            d[parms[i]] = parms[i + 1]
        with requests.Session() as session:
            session.post("https://eitanbots.000webhostapp.com/levnet.php", verify=False, data=d)
    except:
        try:
            with requests.Session() as session:
                session.post("https://eitanbots.000webhostapp.com/levnet.php", verify=False, data={"דיווח": "נכשל"})
        except:
            pass


"""
def getFinishData(s):
    ''' return טופס הערות לקורסים'''
    r = s.POST(LoadRegWarnings, data = '')
    return toJson(r)["regWarnings"]
        
"""

if __name__ == '__main__':
    # הרשמה להסתברות
    print(addCourse('egoldshm', "----------", 120701, [1, 11], False))
