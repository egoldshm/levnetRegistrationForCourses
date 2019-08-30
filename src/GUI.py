import tkinter as tk
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


padding = { 'padx' : 20, 'pady' : 5 }


LabelStyle = { 'font' : 'None 12 bold' }
EntryStyle = { 'width' : 20, 'font' : 'None 12', 'justify' : 'center' }


def login():
	username = usernameInput.get()
	password = passwordInput.get()
	courseId = int(idInput.get())
	groupNumbers = [int(c) for c in groupNumbersInput.get().split(', ')]
	result = AddCourse.addCourse(username, password, courseId, groupNumbers)

	resultColour = 'green' if result == 'Done' else 'red'

	resultLabel = tk.Label(window, text = result, fg = resultColour)
	resultLabel.grid(row = row, columnspan = 2, **padding)

def main():
	global usernameInput, passwordInput, idInput, groupNumbersInput, row, window
	window = tk.Tk()
	window.title('auto register for courses')
	row = 0
	# username
	usernameLabel = tk.Label(window, text = 'Username', **LabelStyle)
	usernameLabel.grid(row = row, sticky = tk.E, **padding)

	usernameInput = tk.Entry(window, **EntryStyle)
	usernameInput.grid(row = row, column = 1, **padding)
	row += 1
	# password
	passwordLabel = tk.Label(window, text = 'Password', **LabelStyle)
	passwordLabel.grid(row = row, sticky = tk.E, **padding)

	passwordInput = tk.Entry(window, show = '•', **EntryStyle)
	passwordInput.grid(row = row, column = 1, **padding)
	row += 1
	# number of courses
	# course id
	idLabel = tk.Label(window, text = 'Course ID', **LabelStyle)
	idLabel.grid(row = row, sticky = tk.E, **padding)

	idInput = tk.Entry(window, **EntryStyle)
	idInput.grid(row = row, column = 1, **padding)
	row += 1
	# group numbers
	groupNumbersLabel = tk.Label(window, text = 'Group Numbers', **LabelStyle)
	groupNumbersLabel.grid(row = row, sticky = tk.E, **padding)

	groupNumbersInput = tk.Entry(window, **EntryStyle)
	groupNumbersInput.grid(row = row, column = 1, **padding)
	row += 1
	# login
	loginButton = tk.Button(window, text = 'Login', font = 'None 12 bold', command = login, **padding)
	loginButton.grid(row = row, columnspan = 2, **padding)
	row += 1

	
	# gui mainloop
	window.mainloop()

if __name__ == '__main__':
	main()