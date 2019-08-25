import tkinter as tk

def login():
	username = usernameInput.get()
	password = passwordInput.get()
	print(password)

def main():
	global usernameInput
	global passwordInput
	window = tk.Tk()
	window.title('auto register for courses')
	# username
	usernameLabel = tk.Label(window, text = 'Username', font = "None 12 bold", padx = 2, pady = 2)
	usernameLabel.grid(row = 0, sticky = tk.E)

	usernameInput = tk.Entry(window, font = 'None 12')
	usernameInput.grid(row = 0, column = 1)
	# password
	passwordLabel = tk.Label(window, text = 'Password', font = 'None 12 bold', padx = 2, pady = 2)
	passwordLabel.grid(row = 1, sticky = tk.E)

	passwordInput = tk.Entry(window, show = '*', font = 'None 12')
	passwordInput.grid(row = 1, column = 1)
	# login
	loginButton = tk.Button(window, text = 'Login', command = login, padx = 2, pady = 2)
	loginButton.grid(row = 3)
	# gui mainloop
	window.mainloop()

if __name__ == '__main__':
	main()