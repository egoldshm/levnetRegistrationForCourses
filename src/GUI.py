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

PADDING_X = 20
PADDING_Y = 5

ENTRY_WIDTH = 20

def login():
	username = usernameInput.get()
	password = passwordInput.get()
	courseId = idInput.get()
	groupNumbers = [int(c) for c in groupNumbersInput.get().split(', ')]
	result = AddCourse.addCourse(username, password, courseId, groupNumbers)
	resultText.set(result)

def main():
	global usernameInput, passwordInput, idInput, groupNumbersInput, resultText
	window = tk.Tk()
	window.title('auto register for courses')
	row = 0
	# username
	usernameLabel = tk.Label(window, text = 'Username', font = 'None 12 bold', padx = PADDING_X, pady = PADDING_Y)
	usernameLabel.grid(row = row, sticky = tk.E)

	usernameInput = tk.Entry(window, width = ENTRY_WIDTH, font = 'None 12', justify = 'center')
	usernameInput.grid(row = row, column = 1, padx = PADDING_X, pady = PADDING_Y)
	row += 1
	# password
	passwordLabel = tk.Label(window, text = 'Password', font = 'None 12 bold', padx = PADDING_X, pady = PADDING_Y)
	passwordLabel.grid(row = row, sticky = tk.E)

	passwordInput = tk.Entry(window, width = ENTRY_WIDTH, show = '•', font = 'None 12', justify = 'center')
	passwordInput.grid(row = row, column = 1, padx = PADDING_X, pady = PADDING_Y)
	row += 1
	# number of courses
	# course id
	idLabel = tk.Label(window, text = 'Course ID', font = 'None 12 bold', padx = PADDING_X, pady = PADDING_Y)
	idLabel.grid(row = row, sticky = tk.E)

	idInput = tk.Entry(window, width = ENTRY_WIDTH, font = 'None 12', justify = 'center')
	idInput.grid(row = row, column = 1, padx = PADDING_X, pady = PADDING_Y)
	row += 1
	# group numbers
	groupNumbersLabel = tk.Label(window, text = 'Group Numbers', font = 'None 12 bold', padx = PADDING_X, pady = PADDING_Y)
	groupNumbersLabel.grid(row = row, sticky = tk.E)

	groupNumbersInput = tk.Entry(window, width = ENTRY_WIDTH, font = 'None 12', justify = 'center')
	groupNumbersInput.grid(row = row, column = 1, padx = PADDING_X, pady = PADDING_Y)
	row += 1
	# login
	loginButton = tk.Button(window, text = 'Login', command = login, padx = PADDING_X, pady = PADDING_Y)
	loginButton.grid(row = row, columnspan = 2, padx = PADDING_X, pady = PADDING_Y)
	row += 1

	# result
	resultText = tk.StringVar(value = '')

	resultLabel = tk.Label(window, textvariable = resultText, padx = PADDING_X, pady = PADDING_Y, fg = 'red')
	resultLabel.grid(row = row, columnspan = 2)
	# gui mainloop
	window.mainloop()

if __name__ == '__main__':
	main()