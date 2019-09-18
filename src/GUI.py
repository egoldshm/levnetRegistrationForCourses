import tkinter as tk
from tkinter import ttk
import Levnet
import AddCourse
from Logo import logo
import time
from datetime import datetime
import StoppableThreading

###############################################################
###                                                         ###
###                                                         ###
### This Code Written By Ariel Darshan And Eytan Goldshmidt ###
###                                                         ###
###             All rights reserved (C)                     ###
###                                                         ###
###                                                         ###
###############################################################


padding = { 'padx' : 10, 'pady' : 5 }

colour = 'purple'

# There is a bug in tkinter that TEntry doesn't work in ttk.Style().configure
EntryStyle = { 'width' : 18, 'font' : 'None 12', 'justify' : 'center' }

class App(tk.Tk):

	def __init__(self, *args, **kwargs):
		self.pages = [LoginPage, MainPage]

		super().__init__(*args, **kwargs)
		self.title('Auto Register For Courses Levnet')
		self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(data = logo))

		self.style = ttk.Style()
		self.style.configure('TFrame', background = colour)
		self.style.configure('Treeview', background = colour)
		self.style.configure('TButton', font = 'None 12 bold', background = colour)
		self.style.configure('TLabel', font = 'None 12 bold', background = colour)
		self.style.configure('TCheckbutton', font = 'None 10 bold', background = colour)

		
		self.container = ttk.Frame(self)
		self.container.pack(side = 'top', fill='both', expand = True)
		self.frames = {}
		self.ShowFrame(LoginPage)

	def ShowFrame(self, page, *args, **kwargs):
		if page not in self.pages:
			return
		if page not in self.frames:
			frame = page(self.container, self, *args, **kwargs)
			self.frames[page] = frame
			frame.grid(row = 0, column = 0, sticky = 'NSEW')
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
		self.Error = tk.Label(self, fg = 'red', **EntryStyle)
		
		header = ttk.Label(self, text = 'Login', font = 'None 16 bold')
		header.grid(columnspan = 1000, **padding, sticky = 'n')

		UsernameLabel = ttk.Label(self, text = 'Username')
		UsernameLabel.grid(**padding, sticky = 'e')

		UsernameInput = ttk.Entry(self, **EntryStyle)
		UsernameInput.focus()
		UsernameInput.grid(row = 1, column = 1, **padding, sticky = 'ew')


		PasswordLabel = ttk.Label(self, text = 'Password')
		PasswordLabel.grid(**padding, sticky = 'e')

		PasswordInput = ttk.Entry(self, show = '•', **EntryStyle)
		PasswordInput.grid(row = 2, column = 1, **padding, sticky = 'ew')

		# Rimon Checkbox
		HasRimon = tk.BooleanVar(value = False)
		RimonCheckbox = ttk.Checkbutton(self, text = 'Using Rimon', onvalue = True, offvalue = False, variable = HasRimon)
		RimonCheckbox.grid(row = 3, column = 1, sticky = 'w', **padding)

		
		login = lambda: self.LoginClick(controller, UsernameInput, PasswordInput, HasRimon.get())
		LoginButton = ttk.Button(self, text = 'Login', default = 'active', command = login)
		controller.bind('<Return>', lambda dummy: login())
		LoginButton.grid(columnspan = 1000, **padding, sticky = 'ns')
	
	def LoginClick(self, controller, UsernameInput, PasswordInput, HasRimon):
		username = UsernameInput.get()
		password = PasswordInput.get()
		with Levnet.Session(username, password, not HasRimon) as s:
			success = s.Login()
		if success:
			controller.ShowFrame(MainPage, username, password, HasRimon)
		else:
			self.Error['text'] = "שם משתמש או סיסמה שגויים"
			self.Error.grid(columnspan = 100, **padding)
			UsernameInput.delete(0, 'end')
			PasswordInput.delete(0, 'end')

class MainPage(ttk.Frame):

	def __init__(self, parent, controller, username, password, Rimon, *args, **kwargs):
		super().__init__(parent)
		self.username = username
		self.password = password
		self.Rimon = Rimon
		self.controller = controller
		self.Courses = []
		self.year = 5780
		self.semester = 1


		ttk.Style().configure('MainPage.TButton')
		BackButton = ttk.Button(self, text = 'Logout', style = 'MainPage.TButton', command = self.LogOut)
		BackButton.grid(row = 0,**padding, sticky = 'w')

		header = ttk.Label(self, text = 'Add Courses', font = 'None 16 bold')
		header.grid(row = 0, column = 1, columnspan = 1000, **padding, sticky = 'w')

		CourseLabel = ttk.Label(self, text = 'Course ID')
		CourseLabel.grid(**padding, sticky = 'e')

		self.CourseInput = ttk.Entry(self, **EntryStyle)
		self.CourseInput.focus()
		self.CourseInput.grid(row = 1, column = 1, **padding, sticky = 'w')


		GroupLabel = ttk.Label(self, text = 'Group Numbers')
		GroupLabel.grid(**padding, sticky = 'e')

		self.GroupInput = ttk.Entry(self, **EntryStyle)
		self.GroupInput.grid(row = 2, column = 1, **padding, sticky = 'w')

		AddButton = ttk.Button(self, text = 'Add Course', style = 'MainPage.TButton', command = self.AddCourse)
		AddButton.grid(column = 1, columnspan = 2, **padding, sticky = 'nsw')

		TreeColumns = ['Course', 'Lesson', 'Lab', 'Result']
		self.CoursesTable = ttk.Treeview(self, columns = tuple(TreeColumns))

		for column in TreeColumns:
			self.CoursesTable.heading(column, text = column)
			self.CoursesTable.column(column, anchor = 'center')
		
		
		self.CoursesTable.column('#0', width = 0)
		self.CoursesTable.grid(columnspan = 3)

		self.RegisterButton = ttk.Button(self, text = 'Register Courses', style = 'MainPage.TButton', command = self.RegisterCourses)
		self.RegisterButton.grid(columnspan = 100, **padding, sticky = 'ns')

		self.ResultLabel = ttk.Label(self, foreground = 'red')



	def AddCourse(self):
		course = self.CourseInput.get()
		groups = self.GroupInput.get(). split(', ')
		with Levnet.Session(self.username, self.password, not self.Rimon) as s:
			s.Login()
			courseName = s.FindCourseName(self.year, self.semester, course)
		self.CoursesTable.insert('', 'end', course, values = tuple([courseName]) + tuple(groups))
		self.Courses.append((course, groups))
		self.CourseInput.delete(0, 'end')
		self.GroupInput.delete(0, 'end')

	def RegisterCourses(self):
		self.ResultLabel.grid(columnspan = 10, **padding)
		def Register():
			with Levnet.Session(self.username, self.password, not self.Rimon) as s:
				s.Login()
				while s.OpenSchedule() == False and not StoppableThreading.currentThread().stopped():
					Now = str(datetime.now()).split('.')[0]
					self.ResultLabel['text'] = f'Last checked if schedule opened: {Now}'
					time.sleep(10.0)
			
			if StoppableThreading.currentThread().stopped():
				return

			for course in self.Courses:
				result = AddCourse.addCourse(self.username, self.password, int(course[0]), [int(x) for x in course[1]], self.Rimon)
				self.CoursesTable.set(course[0], 'Result', result)
		self.RegisterThread = StoppableThreading.Thread(target = Register)
		self.RegisterThread.start()
		
		self.RegisterButton['text'] = 'Cancel'
		self.RegisterButton['command'] = self.Cancel

	def Cancel(self):
		self.RegisterThread.stop()
		
		self.RegisterButton['text'] = 'Register Courses'
		self.RegisterButton['command'] = self.RegisterCourses

	def LogOut(self):
		self.controller.RemoveFrame(self.__class__)



def main():
	app = App()
	app.mainloop()


if __name__ == '__main__':
	main()