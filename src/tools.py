import requests
import json

headers = {'Host' : 'levnet.jct.ac.il', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}


DebugMode = False


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

def GET(session, url):
    '''send GET request to url and do few checks'''
    r = session.get(url, headers = headers, verify = False)
    Assert(r)
    debug(r.text)
    return r

def POST(session, url, data):
    '''send a POST request to url with data and do few checks'''
    r = session.post(url, json = data,  headers = headers, verify = False)
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

