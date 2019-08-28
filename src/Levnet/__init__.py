from tools import *
from URL import *

import requests


class Session(requests.Session):

    def __init__(self, username, password):
        super().__init__(self)
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

    def LoadScheduleTracks(self):
        r = self.POST(CoursesScheduleNew, json = { 'username' : username, 'password' : password })
        return toJson(r)["tracks"]

    def ScheduleWarnings(self):
        r = self.POST(LoadRegWarnings, json = '')
        return toJson(r)["regWarnings"]