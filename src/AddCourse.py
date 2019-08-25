import json
import requests

#############################################################
###                                                       ###
###                                                       ###
### This Code Wrote By Ariel Darshan And Eytan Goldshmidt ###
###                                                       ###
###             All rights reserved (C)                   ###
###                                                       ###
###                                                       ###
#############################################################


#proxy = 'https://localhost:8080'

DebugMode = False

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
        
        r = POST(s, BuildScheduleStart, data = { 'username' : username, 'password' : password })
        whatOpen = toJson(r)["semestersScheduleCreation"]
        if whatOpen == []:
            return "CLOSE"
        
        year = whatOpen[0]["academicYearId"]
        semester = whatOpen[0]["semesterId"]
        print(f"open: year: {year}. semester: {semester}")
        
        POST(s, SelectSemesterForBuildSchedule, data = {"academicYear":year,"semester":semester})
        
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
        
            POST(s, LoadRegWarnings, data = '')#Should to finish
        
            return "Done"

        return "Not Found"

#הרשמה להסתברות
print(addCourse('egoldshm', '----------', 120701, [1,11]))
