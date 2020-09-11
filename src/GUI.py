import tkinter as tk
from tkinter import ttk
import Levnet
import AddCourse
from requests import exceptions as requests_exceptions
from Logo import logo
import time
from datetime import datetime
import StoppableThreading

###############################################################
###                                                         ###
###                                                         ###
### This Code Written By Ariel Darshan And Eytan Goldshmidt ###
###                                                         ###
###               All rights reserved (C)                   ###
###                                                         ###
###                                                         ###
###############################################################
from src.config import YEAR, SEMESTER

padding = {'padx': 10, 'pady': 20}

colour = '#b7d9eb'
SECOND_TO_WAIT = 10
# There is a bug in tkinter that TEntry doesn't work in ttk.Style().configure
EntryStyle = {'width': 18, 'font': 'Gisha 12', 'justify': 'center'}


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.pages = [LoginPage, MainPage]

        super().__init__(*args, **kwargs)
        self.title('Auto Register For Courses Levnet')
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(data=logo))

        self.style = ttk.Style()
        self.style.configure('TFrame', background=colour)
        self.style.configure('Treeview', background=colour)
        self.style.configure('TButton', font='Gisha 12 bold', background=colour)
        self.style.configure('TLabel', font='Gisha 12 bold', background=colour)
        self.style.configure('TCheckbutton', font='Gisha 10 bold', background=colour)

        self.container = ttk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.frames = {}
        self.ShowFrame(LoginPage)

    def ShowFrame(self, page, *args, **kwargs):
        if page not in self.pages:
            return
        if page not in self.frames:
            frame = page(self.container, self, *args, **kwargs)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky='NSEW')
        self.frames[page].tkraise()

    def RemoveFrame(self, page):
        if page in self.pages:
            del self.frames[page]
        self.ShowFrame(LoginPage)

    def destroy(self):
        try:
            self.frames[MainPage].RegisterThread.stop()
            self.frames[MainPage].RegisterThread.join()
        except:
            pass
        return super().destroy()


class LoginPage(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.Error = ttk.Label(self, foreground='red', font='None 12')

        header = ttk.Label(self, text='Login', font='None 16 bold')
        header.grid(columnspan=1000, **padding, sticky='n')

        UsernameLabel = ttk.Label(self, text='Username')
        UsernameLabel.grid(**padding, sticky='e')

        UsernameInput = ttk.Entry(self, **EntryStyle)
        UsernameInput.focus()
        UsernameInput.grid(row=1, column=1, **padding, sticky='ew')

        PasswordLabel = ttk.Label(self, text='Password')
        PasswordLabel.grid(**padding, sticky='e')

        PasswordInput = ttk.Entry(self, show='•', **EntryStyle)
        PasswordInput.grid(row=2, column=1, **padding, sticky='ew')

        CreditLabel = ttk.Label(self, foreground = '#003300', justify="center", font='None 8 bold', text=""" 
        שימו לב - המערכת לא עובדת ב-100% 
        כדאי להיות מוכנים ולוודא בלב-נט שהכל עבד כנדרש
        !אין להפיץ ללא אישור
        😉בלחיצה על הכפתור אתה מאשר את תנאי השימוש
        !סמסטר נפלא""")
        CreditLabel.grid(columnspan=1000, sticky='WENS')

        # Rimon Checkbox
        # HasRimon = tk.BooleanVar(value=False)
        # RimonCheckbox = ttk.Checkbutton(self, text='Using Rimon', onvalue=True, offvalue=False, variable=HasRimon)
        # RimonCheckbox.grid(row=3, column=1, sticky='w', **padding)

        login = lambda: self.LoginClick(controller, UsernameInput, PasswordInput, True)
        self.LoginButton = ttk.Button(self, text='Login', default='active', command=login)
        controller.bind('<Return>', lambda dummy: self.LoginButton.invoke())
        self.LoginButton.grid(columnspan=1000, **padding, sticky='ns')

    def LoginClick(self, controller, UsernameInput, PasswordInput, HasRimon):
        self.Error.grid(columnspan=100, **padding)
        username = UsernameInput.get()
        password = PasswordInput.get()
        self.LoginButton.configure(state="disabled")
        self.LoginButton.update()
        with Levnet.Session(username, password, not HasRimon) as s:
            try:
                success = s.Login()
            except requests_exceptions.SSLError:
                self.Rimon = not self.Rimon
                self.LoginClick(controller, UsernameInput, PasswordInput, self.Rimon)
                self.Error['text'] = 'ודא שבחרת באפשרות הנכונה לגבי רימון'
                return
        if success:
            controller.ShowFrame(MainPage, username, password, HasRimon)

            self.LoginButton.configure(state="normal")
            self.LoginButton.update()
            PasswordInput.delete(0, 'end')
            AddCourse.sendReportToUs("login", "", "username", username)
        else:
            self.Error['text'] = "שם משתמש או סיסמה שגויים"
            UsernameInput.delete(0, 'end')
            PasswordInput.delete(0, 'end')
            self.LoginButton.configure(state="normal")
            self.LoginButton.update()


class MainPage(ttk.Frame):

    def __init__(self, parent, controller, username, password, Rimon, *args, **kwargs):
        super().__init__(parent)
        self.username = username
        self.password = password
        self.Rimon = Rimon
        self.controller = controller
        self.Courses = [(110102, [1])]

        self.year = YEAR
        self.semester = SEMESTER

        if 'semester' in kwargs:
            self.semester = kwargs['semester']

        if 'year' in kwargs:
            self.year = kwargs['year']

        ttk.Style().configure('MainPage.TButton')
        BackButton = ttk.Button(self, text='Logout', style='MainPage.TButton', command=self.LogOut)
        BackButton.grid(row=0, **padding, sticky='w')

        header = ttk.Label(self, text='Add Courses', font='None 16 bold')
        header.grid(row=0, column=1, columnspan=1000, **padding, sticky='w')

        CourseLabel = ttk.Label(self, text='Course ID')
        CourseLabel.grid(**padding, sticky='e')

        self.CourseInput = ttk.Entry(self, **EntryStyle)
        self.CourseInput.focus()
        self.CourseInput.grid(row=1, column=1, **padding, sticky='w')

        GroupLabel = ttk.Label(self, text='Group Numbers')
        GroupLabel.grid(**padding, sticky='e')

        self.LoadingLabel = ttk.Label(self, foreground='red', text="", justify = "center")
        self.LoadingLabel.grid(**padding, columnspan=2, sticky='e')

        self.GroupInput = ttk.Entry(self, **EntryStyle)
        self.GroupInput.grid(row=2, column=1, **padding, sticky='w')

        AddButton = ttk.Button(self, text='Add Course', style='MainPage.TButton', command=self.AddCourse)
        AddButton.grid(column=1, columnspan=2, **padding, sticky='nsw')

        TreeColumns = ['Course', 'Lesson', 'Lab', 'Result']
        self.CoursesTable = ttk.Treeview(self, columns=tuple(TreeColumns))

        for column in TreeColumns:
            self.CoursesTable.heading(column, text=column)
            self.CoursesTable.column(column, anchor='center')

        self.CoursesTable.column('#0', width=0)
        self.CoursesTable.grid(columnspan=3)

        self.RegisterButton = ttk.Button(self, text='Register Courses', style='MainPage.TButton',
                                         command=self.RegisterCourses)
        self.RegisterButton.grid(columnspan=100, **padding, sticky='ns')

        self.ResultLabel = ttk.Label(self, foreground='red')

    def report_error(self, string):
        self.LoadingLabel['text'] = string

    def AddCourse(self):
        course = self.CourseInput.get()
        if not course.isdigit():
            self.report_error("מספר הקורס שגוי. צריך להיות מספר")
            return
        groups = self.GroupInput.get().replace(',', ' ').split()
        if self.GroupInput.get() == "":
            self.report_error("יש להזין מספר קבוצות")
            return
        elif not groups[0].isdigit():
            self.report_error("מספר הקבוצות שגוי. צריך להיות מספר אחד או שניים מופרדים בפסיקים או רווחים")
            return
        elif len(groups) > 1 and not groups[1].isdigit():
            self.report_error("מספר הקבוצות שגוי. צריך להיות מספר אחד או שניים מופרדים בפסיקים או רווחים")
            return
        elif len(groups) not in (1, 2):
            self.report_error("מספר הקבוצות שגוי. צריך להיות מספר אחד או שניים מופרדים בפסיקים או רווחים")
            return

        def checkCourse():
            with Levnet.Session(self.username, self.password, not self.Rimon) as s:
                try:
                    s.Login()
                    courseName = s.FindCourseName(self.year, self.semester, course)
                    detail = s.FindLecturersAndTimes(self.year, self.semester, course, groups)
                    if courseName and detail:
                        print(detail, groups)
                        detail = [f"{lecturer} - {group}" for lecturer, group in zip(detail, groups)]
                        self.CoursesTable.insert('', 'end', course, values=tuple([courseName]) + tuple(detail))
                        self.report_error("")
                        AddCourse.sendReportToUs("check course", "", "username", self.username, "course", course,
                                                 "details", str(detail + groups))
                    else:
                        self.report_error('לא נמצא קורס עם הפרטים הללו')

                except:
                    self.report_error("בעיה בטעינת הנתונים על הקורס. נסה שוב.")

                self.GroupInput.configure(state="normal")
                self.GroupInput.update()
                self.CourseInput.configure(state="normal")
                self.CourseInput.update()
                self.CourseInput.delete(0, 'end')
                self.GroupInput.delete(0, 'end')

        self.GroupInput.configure(state="disabled")
        self.GroupInput.update()
        self.CourseInput.configure(state="disabled")
        self.CourseInput.update()

        self.report_error('טוען נתונים על הקורס')

        self.CheckThreading = StoppableThreading.Thread(target=checkCourse)
        self.CheckThreading.start()

        self.Courses.append((course, groups))

    def RegisterCourses(self):
        self.ResultLabel.grid(columnspan=10, **padding)

        def Register():
            with Levnet.Session(self.username, self.password, not self.Rimon) as s:
                s.Login()
                while not s.OpenSchedule():
                    Now = str(datetime.now()).split('.')[0]
                    self.ResultLabel['text'] = f'Last checked if schedule opened: {Now}'
                    for _ in range(SECOND_TO_WAIT):
                        if StoppableThreading.currentThread().stopped():
                            return
                        time.sleep(1.0)
            for course in self.Courses:
                result = AddCourse.addCourse(self.username, self.password, int(course[0]), [int(x) for x in course[1]],
                                             self.Rimon)
                if course[0] in self.CoursesTable.get_children():
                    self.CoursesTable.set(course[0], 'Result', result)
                AddCourse.sendReportToUs("added course", "", "username", self.username, "course", str(course[0]) + str(course[1]), "result",
                                         result)

        self.RegisterThread = StoppableThreading.Thread(target=Register)
        self.RegisterThread.start()

        self.RegisterButton['text'] = 'Cancel'
        self.RegisterButton['command'] = self.Cancel

    def Cancel(self):
        self.RegisterThread.stop()
        for i in range(int(SECOND_TO_WAIT + 1.0), 0, -1):
            self.RegisterButton.configure(state="disabled")
            self.RegisterButton['text'] = "סבלנות! חכה עוד {} שניות".format(i)
            self.RegisterButton.update()
            time.sleep(1.0)

        self.RegisterButton['text'] = 'Register Courses'
        self.RegisterButton.configure(state="normal")
        self.RegisterButton['command'] = self.RegisterCourses

    def LogOut(self):
        self.controller.RemoveFrame(self.__class__)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
