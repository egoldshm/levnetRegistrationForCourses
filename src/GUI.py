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

		UsernameInput = tk.Entry(self, font = 'None 12', justify = 'center')
		UsernameInput.grid(row = 1, column = 1, pady = 10, padx = 10, sticky = 'ew')


		PasswordLabel = tk.Label(self, text = 'Password', font = 'None 12 bold')
		PasswordLabel.grid(pady = 10, padx = 10, sticky = 'e')

		PasswordInput = tk.Entry(self, show = '•', font = 'None 12', justify = 'center')
		PasswordInput.grid(row = 2, column = 1, pady = 10, padx = 10, sticky = 'ew')


		login = lambda: controller.ShowFrame(MainPage, username = UsernameInput.get(), password = PasswordInput.get())
		ttk.Style().configure('Login.TButton', font = 'None 12 bold')
		LoginButton = ttk.Button(self, text = 'Login', style = 'Login.TButton', command = login)
		LoginButton.grid(columnspan = 1000, pady = 10, padx = 10, sticky = 'ns')

class MainPage(tk.Frame):

	def __init__(self, parent, controller, *args, username = '', password = '', **kwargs):
		super().__init__(parent)
		self.username = username
		self.password = password
		self.controller = controller


		ttk.Style().configure('MainPage.TButton', font = 'None 12 bold')
		BackButton = ttk.Button(self, text = '<', style = 'MainPage.TButton', command = self.LogOut)
		BackButton.grid(row = 0,pady = 10, padx = 10, sticky = 'w')

		header = tk.Label(self, text = username, font = 'None 16 bold')
		header.grid(row = 0, column = 1, columnspan = 1000, pady = 10, padx = 10, sticky = 'nsew')

		CourseLabel = tk.Label(self, text = 'Course ID', font = 'None 12 bold')
		CourseLabel.grid(pady = 10, padx = 10, sticky = 'e')

		CourseInput = tk.Entry(self, font = 'None 12', justify = 'center')
		CourseInput.grid(row = 1, column = 1, pady = 10, padx = 10, sticky = 'ew')


		GroupLabel = tk.Label(self, text = 'Group Numbers', font = 'None 12 bold')
		GroupLabel.grid(pady = 10, padx = 10, sticky = 'e')

		GroupInput = tk.Entry(self, font = 'None 12', justify = 'center')
		GroupInput.grid(row = 2, column = 1, pady = 10, padx = 10, sticky = 'ew')

		click = lambda: self.RegisterCourse(int(CourseInput.get()), [int(x) for x in GroupInput.get().split(', ')])
		RegisterButton = ttk.Button(self, text = 'Register Course', style = 'MainPage.TButton', command = click)
		RegisterButton.grid(columnspan = 1000, pady = 10, padx = 10, sticky = 'ns')

	def RegisterCourse(self, course, groups):
		result = AddCourse.addCourse(self.username, self.password, course, groups)
		ResultLabel = tk.Label(self, text = result, fg = 'green' if result == 'Done' else 'red')
		ResultLabel.grid(columnspan = 1000)

	def LogOut(self):
		self.controller.RemoveFrame(self.__class__)


def main():
	app = App()
	app.mainloop()


if __name__ == '__main__':
	main()