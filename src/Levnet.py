from tools import *
from URL import *

import requests


class Session(requests.Session):

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def GET(self, url):
        r = self.get(url, headers = headers, verify = verify)
        Assert(r)
        debug(r.text)
        return r

    def POST(self, url, json):
        r = self.post(url, json = json, headers = headers, verify = verify)
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