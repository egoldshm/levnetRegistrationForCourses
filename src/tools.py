import requests
import json

headers = {'Host' : 'levnet.jct.ac.il', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}

loginUrl = 'https://levnet.jct.ac.il/api/home/login.ashx?action=TryLogin'
ScheduleStart = 'https://levnet.jct.ac.il/Student/Schedule/Start.aspx'
BuildScheduleStart = 'https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=LoadDataForBuildScheduleStart'

DebugMode = False
StrictMode = False # If set to true, program will defualt to terminating more
verify = False



def PrintError(message):
    print(' '.join(message.split(' ')[::-1]))

def Assert(request):
    if not request.ok:
        print(request.text)
        if StrictMode:
            exit(1)
        else:
            print('^^^^ERROR in request. response is above^^^^')
    try:
        if 'error' in json.loads(request.content):
            PrintError(json.loads(request.content)['error'])
            if StrictMode:
                exit(1)
    except json.decoder.JSONDecodeError:
        pass

def debug(message):
    if DebugMode:
        input(message)

def toJson(x):
    return json.loads(x.content)

def GET(session, url):
    '''send GET request to url and do few checks'''
    r = session.get(url, headers = headers, verify = verify)
    Assert(r)
    debug(r.text)
    return r

def POST(session, url, data):
    '''send a POST request to url with data and do few checks'''
    r = session.post(url, json = data,  headers = headers, verify = verify)
    Assert(r)
    debug(r.text)
    return r

def getIdOfCourse(json,courseId):
    '''get element of course, from number of the couse - find the ID'''
    courseWithRightId = list(filter(lambda i: i["parentCourseNumber"] == courseId, toJson(json)["coursesForTrack"]))
    if len(courseWithRightId) == 0:
        return -1
    return courseWithRightId[0]["programMemberId"]

def getIdOfGroups(json, groupNumbers):
    groups = toJson(json)["coursesForProgram"][0]["groups"]
    id = toJson(json)["coursesForProgram"][0]["id"]
    courseWithRightId = list(filter(lambda i: i["groupNumber"] in groupNumbers, groups))
    if len(courseWithRightId) != len(groupNumbers):
        return -1
    ids = list(map(lambda j: j["id"], courseWithRightId))
    return {"actualCourseId":id,"selectedGroups":ids}


class Levnet:
    class Session(requests.Session):

        def __init__(self, username, password):
            requests.Session.__init__(self)
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

        def ScheduleWarnings(self):
            r = self.POST(LoadRegWarnings, json = '')
            return toJson(r)["regWarnings"]