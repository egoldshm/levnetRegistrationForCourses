import requests
import json

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