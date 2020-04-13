from tkinter import *
import tkinter.scrolledtext as tkst
import tkinter as tk


from settingsGA import gaParams

def info_GUI():
	with open('GA-statistics.txt', 'r') as f:
		mytext = f.read()
		root = Tk()

		root.title("STATISTICS")
		root.geometry('700x500+100+100')

		frame = tk.Frame(master = root, bg = 'grey')
		frame.pack(fill='both', expand='yes')
		text = tkst.ScrolledText(
		    master = frame,
		    wrap   = tk.WORD,
		    width  = 700,
		    height = 500
		)

		text.pack()
		text.insert(1.0, mytext)
		root.mainloop()

def get_settings() -> gaParams:	
	root = Tk()
	root.title("Settings")
	root.geometry('500x250+100+100')
	 
	f = StringVar()
	chromosomes_number = IntVar()
	generations_number = IntVar()
	optimizer = StringVar()
	mutation = BooleanVar()

	chromosomes_number.set(4)
	generations_number.set(10)
	optimizer.set('min')
	mutation.set(0)

	chk = Checkbutton(text="Mutation", variable=mutation, onvalue=1, offvalue=0)
	 
	f_label = Label(text="Input f(x, y) in python format:", font='arial 13')
	chromosomes_number_label = Label(text="Input chromosomes number (multiple of 4):", font='arial 13')
	generations_number_label = Label(text="Input generations number:", font='arial 13')
	optimizer_label = Label(text="Input optimizer (min or max):", font='arial 13')
	 
	f_label.grid(row=0, column=0, sticky="w")
	chromosomes_number_label.grid(row=1, column=0, sticky="w")
	generations_number_label.grid(row=2, column=0, sticky="w")
	optimizer_label.grid(row=3, column=0, sticky="w")
	 
	f_entry = Entry(textvariable=f)
	chromosomes_number_entry = Entry(textvariable=chromosomes_number)
	generations_number_entry = Entry(textvariable=generations_number)
	optimizer_entry = Entry(textvariable=optimizer)
	 
	f_entry.grid(row=0,column=1, padx=5, pady=5)
	chromosomes_number_entry.grid(row=1,column=1, padx=5, pady=5)
	generations_number_entry.grid(row=2,column=1, padx=5, pady=5)
	optimizer_entry.grid(row=3,column=1, padx=5, pady=5)
	chk.grid(row=4, column=1)
	c = Checkbutton(text="Mutation", variable=mutation, onvalue=1, offvalue=0)


	submit_button = Button(text=" Submit ", command=root.destroy, font='arial 17', 
							bg='green', state='active', bd=3, height=2, width=8)

	submit_button.grid(row=7,column=0, padx=10, pady=10, sticky="e")

	root.mainloop()
	return gaParams(f.get(), chromosomes_number.get(), generations_number.get(), mutation.get(), optimizer.get())

def error_GUI():
	root = Tk()
	root.title("ERROR")
	root.geometry('300x150+100+100')
	text = Text(width=20, height=3, font='arial 20')
	text.insert(1.0, "\nЧТО-ТО ПОШЛО НЕ ТАК!")
	text.pack()
	ok_button = Button(text=" OK ", command=root.destroy, font='arial 17', 
							bg='red', state='active', bd=3, height=2, width=8)
	ok_button.pack()
	root.mainloop()


