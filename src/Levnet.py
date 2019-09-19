#from tools import *
from tools import Assert, debug, toJson

import requests

###############################################################
###                                                         ###
###                                                         ###
### This Code Written By Ariel Darshan And Eytan Goldshmidt ###
###                                                         ###
###               All rights reserved (C)                   ###
###                                                         ###
###                                                         ###
###############################################################

headers = {'Host' : 'levnet.jct.ac.il', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
loginUrl = 'https://levnet.jct.ac.il/api/home/login.ashx?action=TryLogin'
ScheduleStart = 'https://levnet.jct.ac.il/Student/Schedule/Start.aspx'
BuildScheduleStart = 'https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=LoadDataForBuildScheduleStart'
SelectSemesterForBuildSchedule = 'https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=SelectSemesterForBuildSchedule'
CoursesScheduleNew = 'https://levnet.jct.ac.il/Student/Schedule/CoursesScheduleNew.aspx'
LoadScheduleData = 'https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=LoadData'
LoadCoursesForTrack = 'https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=LoadCoursesForTrack'
LoadCoursesForProgram = 'https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=LoadCoursesForProgram'
SaveGroupsSelection = 'https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=SaveGroupsSelection'
LoadRegWarnings = 'https://levnet.jct.ac.il/api/student/RegWarningsForCourses.ashx?action=LoadRegWarnings'
ActualCourse = 'https://levnet.jct.ac.il/api/common/actualCourses.ashx?action=LoadActualCourses'

class Session(requests.Session):

    def __init__(self, username, password, verify):
        super().__init__()
        self.username = username
        self.password = password
        self.verify = verify

    def GET(self, url):
        r = self.get(url, headers = headers, verify = self.verify)
        Assert(r)
        debug(r.text)
        return r

    def POST(self, url, json):
        r = self.post(url, json = json, headers = headers, verify = self.verify)
        Assert(r)
        debug(r.text)
        return r

    def Login(self):
        r = self.POST(loginUrl, json = { 'username' : self.username, 'password' : self.password })
        return toJson(r)['success']

    def OpenSchedule(self):
        self.GET(ScheduleStart)
        r = self.POST(BuildScheduleStart, json = { 'username' : self.username, 'password' : self.password })

        whatOpen = toJson(r)["semestersScheduleCreation"]

        if whatOpen == []:
            return False

        year = whatOpen[0]["academicYearId"]
        semester = whatOpen[0]["semesterId"]
        return {"academicYear":year,"semester":semester}

    def SelectSemesterForSchedule(self, time):
        self.POST(SelectSemesterForBuildSchedule, json = time)

    def LoadScheduleTracks(self):
        r = self.POST(LoadScheduleData, json = { 'username' : self.username, 'password' : self.password })
        return toJson(r)["tracks"]

    def LoadTrackCourses(self, track):
        return self.POST(LoadCoursesForTrack, json = {"selectedTrack": track["id"]})

    def LoadProgramCourses(self, program):
        r = self.POST(LoadCoursesForProgram, json = {"programMemberId":program})
        return r

    def CoursesSchedule(self):
        return self.GET(CoursesScheduleNew)

    def SelectGroups(self, groupIDs):
        return self.POST(SaveGroupsSelection, json = groupIDs)

    def ScheduleWarnings(self):
        r = self.POST(LoadRegWarnings, json = '')
        return toJson(r)["regWarnings"]
    
    def FindCourseName(self, year, semester, id):
        result = self.POST(ActualCourse, json = {"selectedAcademicYear":year,"selectedSemester":semester,"selectedExtension":None,"selectedCategory":None,"freeSearch":None})
        for page in range(toJson(result)["totalPages"]):
            result = self.POST(ActualCourse, json = {"current": page + 1, "selectedAcademicYear":year,"selectedSemester":semester,"selectedExtension":None,"selectedCategory":None,"freeSearch":None})
            for item in toJson(result)["items"]:
                if item["courseFullNumber"].split(".")[0] == str(id):
                    return item["courseName"]