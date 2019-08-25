import tkinter as tk
import AddCourse

def login():
	username = usernameInput.get()
	password = passwordInput.get()
	courseId = idInput.get()
	groupNumbers = [int(c) for c in groupNumbersInput.get().split(', ')]
	result = AddCourse.addCourse(username, password, courseId, groupNumbers)
	resultText.set(result)


def main():
	global usernameInput
	global passwordInput
	global idInput
	global groupNumbersInput
	global resultText
	window = tk.Tk()
	window.title('auto register for courses')
	row = 0
	# username
	usernameLabel = tk.Label(window, text = 'Username', font = 'None 12 bold', padx = 2, pady = 2)
	usernameLabel.grid(row = row, sticky = tk.E)

	usernameInput = tk.Entry(window, font = 'None 12')
	usernameInput.grid(row = row, column = 1)
	row += 1
	# password
	passwordLabel = tk.Label(window, text = 'Password', font = 'None 12 bold', padx = 2, pady = 2)
	passwordLabel.grid(row = row, sticky = tk.E)

	passwordInput = tk.Entry(window, show = '•', font = 'None 12')
	passwordInput.grid(row = row, column = 1)
	row += 1
	# number of courses
	# course id
	idLabel = tk.Label(window, text = 'Course ID', font = 'None 12 bold', padx = 2, pady = 2)
	idLabel.grid(row = row, sticky = tk.E)

	idInput = tk.Entry(window, font = 'None 12')
	idInput.grid(row = row, column = 1)
	row += 1
	# group numbers
	groupNumbersLabel = tk.Label(window, text = 'Group Numbers', font = 'None 12 bold', padx = 2, pady = 2)
	groupNumbersLabel.grid(row = row, sticky = tk.E)

	groupNumbersInput = tk.Entry(window, font = 'None 12')
	groupNumbersInput.grid(row = row, column = 1)
	row += 1
	# login
	loginButton = tk.Button(window, text = 'Login', command = login, padx = 2, pady = 2)
	loginButton.grid(row = row)
	row += 1

	# result
	resultText = tk.StringVar(value = '')

	resultLabel = tk.Label(window, textvariable = resultText, padx = 2, pady = 2)
	resultLabel.grid(row = row)
	# gui mainloop
	window.mainloop()

if __name__ == '__main__':
	main()