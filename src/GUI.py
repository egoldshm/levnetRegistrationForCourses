import tkinter as tk
from tkinter import ttk
import Levnet
import AddCourse


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
LabelStyle = { 'font' : 'None 12 bold' }
EntryStyle = { 'width' : 20, 'font' : 'None 12', 'justify' : 'center' }

class App(tk.Tk):

	def __init__(self, *args, **kwargs):
		self.pages = [LoginPage, MainPage]

		super().__init__(*args, **kwargs)
		self.title('Auto Register For Courses Levnet')

		self.container = tk.Frame(self)
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


class LoginPage(tk.Frame):

	def __init__(self, parent, controller):
		super().__init__(parent)
		self.Error = tk.Label(self, fg = 'red', **EntryStyle)
		
		header = tk.Label(self, text = 'Login', font = 'None 16 bold')
		header.grid(columnspan = 1000, **padding, sticky = 'nsew')

		UsernameLabel = tk.Label(self, text = 'Username', **LabelStyle)
		UsernameLabel.grid(**padding, sticky = 'e')

		UsernameInput = ttk.Entry(self, **EntryStyle)
		UsernameInput.grid(row = 1, column = 1, **padding, sticky = 'ew')


		PasswordLabel = tk.Label(self, text = 'Password', **LabelStyle)
		PasswordLabel.grid(**padding, sticky = 'e')

		PasswordInput = ttk.Entry(self, show = '•', **EntryStyle)
		PasswordInput.grid(row = 2, column = 1, **padding, sticky = 'ew')

		# Rimon Checkbox
		RimonLabel = tk.Label(self, text = 'Using Rimon', **LabelStyle)
		RimonLabel.grid(row = 3, sticky = 'e', **padding)

		HasRimon = tk.BooleanVar(value = False)
		RimonCheckbox = ttk.Checkbutton(self, onvalue = True, offvalue = False, variable = HasRimon)
		RimonCheckbox.grid(row = 3, column = 1, sticky = 'w', **padding)

		
		login = lambda: self.LoginClick(controller, UsernameInput, PasswordInput, HasRimon.get())
		ttk.Style().configure('Login.TButton', **LabelStyle)
		LoginButton = ttk.Button(self, text = 'Login', style = 'Login.TButton', default = 'active', command = login)
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

class MainPage(tk.Frame):

	def __init__(self, parent, controller, username, password, Rimon, *args, **kwargs):
		super().__init__(parent)
		self.username = username
		self.password = password
		self.Rimon = Rimon
		self.controller = controller
		self.Courses = []


		ttk.Style().configure('MainPage.TButton', **LabelStyle)
		BackButton = ttk.Button(self, text = 'Logout', style = 'MainPage.TButton', command = self.LogOut)
		BackButton.grid(row = 0,**padding, sticky = 'w')

		header = tk.Label(self, text = 'Add Courses', font = 'None 16 bold')
		header.grid(row = 0, column = 1, columnspan = 1000, **padding, sticky = 'w')

		CourseLabel = tk.Label(self, text = 'Course ID', **LabelStyle)
		CourseLabel.grid(**padding, sticky = 'e')

		self.CourseInput = tk.Entry(self, font = 'None 12', justify = 'center', width = 15)
		self.CourseInput.focus()
		self.CourseInput.grid(row = 1, column = 1, **padding, sticky = 'w')


		GroupLabel = tk.Label(self, text = 'Group Numbers', **LabelStyle)
		GroupLabel.grid(**padding, sticky = 'e')

		self.GroupInput = tk.Entry(self, font = 'None 12', justify = 'center', width = 15)
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

		RegisterButton = ttk.Button(self, text = 'Register Courses', style = 'MainPage.TButton', command = self.RegisterCourses)
		RegisterButton.grid(columnspan = 100, **padding, sticky = 'ns')




	def AddCourse(self):
		course = self.CourseInput.get()
		groups = self.GroupInput.get(). split(', ')
		self.CoursesTable.insert('', 'end', course, values = tuple([course]) + tuple(groups))
		self.Courses.append((course, groups))
		self.CourseInput.delete(0, 'end')
		self.GroupInput.delete(0, 'end')

	def RegisterCourses(self):
		for course in self.Courses:
			result = AddCourse.addCourse(self.username, self.password, int(course[0]), [int(x) for x in course[1]], self.Rimon)
			self.CoursesTable.set(course[0], 'Result', result)

	def LogOut(self):
		self.controller.RemoveFrame(self.__class__)



def main():
	app = App()
	app.mainloop()


if __name__ == '__main__':
	main()