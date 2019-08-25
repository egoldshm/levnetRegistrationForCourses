import json
import requests

######################

######################


#proxy = 'https://localhost:8080'

DebugMode = False

year = 5780
semester = 1
'''
[V]POST    /api/home/login.ashx?action=TryLogin
[V]GET:    /Student/Schedule/Start.aspx
[V]POST    /api/student/buildSchedule.ashx?action=LoadDataForBuildScheduleStart
[X]GET:    /api/student/status.ashx?action=GetBlockingReasons
[V]POST    /api/student/buildSchedule.ashx?action=SelectSemesterForBuildSchedule
[V]GET:    /Student/Schedule/CoursesScheduleNew.aspx
[V]POST    /api/student/buildSchedule.ashx?action=LoadData
[V]POST    /api/student/buildSchedule.ashx?action=LoadCoursesForTrack
[V]POST    /api/student/buildSchedule.ashx?action=LoadCoursesForProgram
[V]POST    /api/student/buildSchedule.ashx?action=SaveGroupsSelection
'''

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

def PrintError(message):
    print(' '.join(message.split(' ')[::-1]))

def Assert(request):
    if not request.ok:
        print(request.text)
        exit(1)
    try:
        if 'error' in json.loads(request.content):
            PrintError(json.loads(request.content)['error'])
            exit(1)
    except json.decoder.JSONDecodeError:
        pass

def debug(message):
    if DebugMode:
        input(message)

def toJson(x):
    return json.loads(x.content)

def getIdOfCourse(json,courseId):
    return list(map(lambda j: j["programMemberId"], filter(lambda i: i["parentCourseNumber"] == courseId, toJson(json)["coursesForTrack"])))[0]

def getIdOfGroups(json, groupNumbers):
    groups = toJson(json)["coursesForProgram"][0]["groups"]
    id = toJson(json)["coursesForProgram"][0]["id"]
    ids = list(map(lambda j: j["id"], filter(lambda i: i["groupNumber"] in groupNumbers, groups)))
    return {"actualCourseId":id,"selectedGroups":ids}
    
def GET(session, url):
    r = session.get(url, headers = headers)
    Assert(r)
    debug(r.text)
    return r

def POST(session, url, data):
    r = session.post(url, json = data, headers = headers)
    Assert(r)
    debug(r.text)
    return r
    

def addCourse(username, password, courseId, groupNumbers):
    with requests.Session() as s:
        POST(s, loginUrl, data = { 'username' : username, 'password' : password })
        
        GET(s, ScheduleStart)
        
        POST(s, BuildScheduleStart, data = { 'username' : username, 'password' : password })
        
        POST(s, SelectSemesterForBuildSchedule, data = {"academicYear":year,"semester":semester})
        
        GET(s, CoursesNew)
        
        POST(s, CoursesScheduleNew, data = { 'username' : username, 'password' : password })
        
        r = POST(s, LoadCoursesForTrack, data = {"selectedTrack":33})
        
        id = getIdOfCourse(r,courseId)
        r = POST(s, LoadCoursesForProgram, data = {"programMemberId":id})

        idOfGroups = getIdOfGroups(r,groupNumbers)
        
        print(f"Register to: {idOfGroups}")#Until Now - Work fine.
        
        POST(s, SaveGroupsSelection, data = idOfGroups)#problem here
        
        POST(s, LoadRegWarnings, data = '')#Should to finish
        
        print('done')

if __name__ == "__main__":
	#הרשמה להסתברות
	addCourse('ardarsha', '--CENSORED--', 120701, [1,11])
