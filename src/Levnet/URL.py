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