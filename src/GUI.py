import tkinter as tk
from tkinter import ttk
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


'''
padding = { 'padx' : 20, 'pady' : 5 }
LabelStyle = { 'font' : 'None 12 bold' }
EntryStyle = { 'width' : 20, 'font' : 'None 12', 'justify' : 'center' }
'''

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
		header = tk.Label(self, text = 'Login', font = 'None 16 bold')
		header.grid(columnspan = 1000, pady = 10, padx = 10, sticky = 'nsew')

		UsernameLabel = tk.Label(self, text = 'Username', font = 'None 12 bold')
		UsernameLabel.grid(pady = 10, padx = 10, sticky = 'e')

		UsernameInput = tk.Entry(self, font = 'None 12', justify = 'center', width = 20)
		UsernameInput.grid(row = 1, column = 1, pady = 10, padx = 10, sticky = 'ew')


		PasswordLabel = tk.Label(self, text = 'Password', font = 'None 12 bold')
		PasswordLabel.grid(pady = 10, padx = 10, sticky = 'e')

		PasswordInput = tk.Entry(self, show = '•', font = 'None 12', justify = 'center', width = 20)
		PasswordInput.grid(row = 2, column = 1, pady = 10, padx = 10, sticky = 'ew')


		login = lambda: controller.ShowFrame(MainPage, username = UsernameInput.get(), password = PasswordInput.get())
		ttk.Style().configure('Login.TButton', font = 'None 12 bold')
		LoginButton = ttk.Button(self, text = 'Login', style = 'Login.TButton', default = 'active', command = login)
		controller.bind('<Return>', lambda dummy: login())
		LoginButton.grid(columnspan = 1000, pady = 10, padx = 10, sticky = 'ns')

class MainPage(tk.Frame):

	def __init__(self, parent, controller, *args, username = '', password = '', **kwargs):
		super().__init__(parent)
		self.username = username
		self.password = password
		self.controller = controller
		self.Courses = []


		ttk.Style().configure('MainPage.TButton', font = 'None 12 bold')
		BackButton = ttk.Button(self, text = 'Logout', style = 'MainPage.TButton', command = self.LogOut)
		BackButton.grid(row = 0,pady = 10, padx = 10, sticky = 'w')

		header = tk.Label(self, text = 'Add Courses', font = 'None 16 bold')
		header.grid(row = 0, column = 1, columnspan = 1000, pady = 10, padx = 10, sticky = 'w')

		CourseLabel = tk.Label(self, text = 'Course ID', font = 'None 12 bold')
		CourseLabel.grid(pady = 10, padx = 10, sticky = 'e')

		self.CourseInput = tk.Entry(self, font = 'None 12', justify = 'center', width = 15)
		self.CourseInput.focus()
		self.CourseInput.grid(row = 1, column = 1, pady = 10, padx = 10, sticky = 'w')


		GroupLabel = tk.Label(self, text = 'Group Numbers', font = 'None 12 bold')
		GroupLabel.grid(pady = 10, padx = 10, sticky = 'e')

		self.GroupInput = tk.Entry(self, font = 'None 12', justify = 'center', width = 15)
		self.GroupInput.grid(row = 2, column = 1, pady = 10, padx = 10, sticky = 'w')

		AddButton = ttk.Button(self, text = 'Add Course', style = 'MainPage.TButton', command = self.AddCourse)
		AddButton.grid(column = 1, columnspan = 2, pady = 10, padx = 10, sticky = 'nsw')

		TreeColumns = ['Course', 'Lesson', 'Lab', 'Result']
		self.CoursesTable = ttk.Treeview(self, columns = tuple(TreeColumns))

		for column in TreeColumns:
			self.CoursesTable.heading(column, text = column)
			self.CoursesTable.column(column, anchor = 'center')
		
		
		self.CoursesTable.column('#0', width = 0)
		self.CoursesTable.grid(columnspan = 3)

		RegisterButton = ttk.Button(self, text = 'Register Courses', style = 'MainPage.TButton', command = self.RegisterCourses)
		RegisterButton.grid(columnspan = 100, pady = 10, padx = 10, sticky = 'ns')




	def AddCourse(self):
		course = self.CourseInput.get()
		groups = self.GroupInput.get(). split(', ')
		self.CoursesTable.insert('', 'end', course, values = tuple([course]) + tuple(groups))
		self.Courses.append((course, groups))
		self.CourseInput.delete(0, 'end')
		self.GroupInput.delete(0, 'end')

	def RegisterCourses(self):
		for course in self.Courses:
			result = AddCourse.addCourse(self.username, self.password, int(course[0]), [int(x) for x in course[1]])
			self.CoursesTable.set(course[0], 'Result', result)

		
		'''
		if self.DispRes:
			self.ResultLabel.grid_remove()
		result = AddCourse.addCourse(self.username, self.password, course, groups)
		self.ResultLabel = tk.Label(self, text = result, fg = 'green' if result == 'Done' else 'red')
		self.ResultLabel.grid(columnspan = 2)
		self.DispRes = True
		'''

	def LogOut(self):
		self.controller.RemoveFrame(self.__class__)



def main():
	app = App()
	app.mainloop()


if __name__ == '__main__':
	main()