import tkinter.scrolledtext as tkst
import tkinter as tk

from tkinter import *
from accessify import protected

from settingsGA import gaParams
from optimizer import OptimizerGA
from func import Func


class gaGUI():
	def __init__(self):
		self.root = Tk()
		self.root.title("Settings")
		self.root.geometry('550x300+100+100')
		self.root.configure(bg='white')
		# photo = PhotoImage(file = "logo.png")
		# w = Label(self.root, image=photo)
		# w.grid()
		self.f = StringVar()
		self.chromosomes_number = IntVar()
		self.generations_number = IntVar()
		self.optimizer = StringVar()
		self.mutation = BooleanVar()
		self.mutation_range = IntVar()
		self.statistics = BooleanVar()
		self.save = BooleanVar()
		self.plot = BooleanVar()

		self.chromosomes_number.set(4)
		self.generations_number.set(10)
		self.optimizer.set('min')
		self.mutation.set(1)
		self.mutation_range.set(2)
		self.statistics.set(1)
		self.plot.set(1)
		self.save.set(0)

		self.chk1 = Checkbutton(text="Mutation", variable=self.mutation, onvalue=1, offvalue=0)
		self.chk2 = Checkbutton(text="Show statistics", variable=self.statistics, onvalue=1, offvalue=0)
		self.chk3 = Checkbutton(text="Save all files", variable=self.save, onvalue=1, offvalue=0)
		self.chk4 = Checkbutton(text="Show plot", variable=self.plot, onvalue=1, offvalue=0)
		 
		self.f_label = Label(text="Input f(x, y) in python format:", font='arial 13')
		self.chromosomes_number_label = Label(text="Input individs number (multiple of 4):", font='arial 13')
		self.generations_number_label = Label(text="Input generations number:", font='arial 13')
		self.mutation_range_label = Label(text="Input mutation range:", font='arial 13')
		self.optimizer_label = Label(text="Input optimizer (min or max):", font='arial 13')
		 
		self.f_label.grid(row=0, column=0, sticky="w")
		self.chromosomes_number_label.grid(row=1, column=0, sticky="w")
		self.generations_number_label.grid(row=2, column=0, sticky="w")
		self.optimizer_label.grid(row=3, column=0, sticky="w")
		self.mutation_range_label.grid(row=5, column=0, sticky="w")

		self.f_entry = Entry(textvariable=self.f)
		self.chromosomes_number_entry = Entry(textvariable=self.chromosomes_number)
		self.generations_number_entry = Entry(textvariable=self.generations_number)
		self.mutation_range_entry = Entry(textvariable=self.mutation_range)
		self.optimizer_entry = Entry(textvariable=self.optimizer)
		 
		self.f_entry.grid(row=0,column=1, padx=5, pady=5)
		self.chromosomes_number_entry.grid(row=1,column=1, padx=5, pady=5)
		self.generations_number_entry.grid(row=2,column=1, padx=5, pady=5)
		self.optimizer_entry.grid(row=3,column=1, padx=5, pady=5)
		self.chk1.grid(row=6, column=0, padx=1, pady=1)
		self.mutation_range_entry.grid(row=5, column=1, padx=5, pady=5)
		self.chk2.grid(row=6, column=1, padx=1, pady=1)
		self.chk3.grid(row=7, column=1, padx=1, pady=1)
		self.chk4.grid(row=7, column=0, padx=1, pady=1)


		self.submit_button = Button(text=" calculate ", command=self.gaInfo, font='arial 17', 
								bg='green', state='active', bd=5, height=1, width=30)

		self.submit_button.grid(row=12, column=0, columnspan=3, pady=8)

		self.root.mainloop()

	def gaInfo(self):
		try:
			function = Func(self.f_entry.get())

			optimizer = OptimizerGA(function)
			optimizer.startGA(	chromosomes_number=int(self.chromosomes_number_entry.get()), 
								generations_number=int(self.generations_number_entry.get()), 
								mutation=self.mutation.get(), mutation_range=self.mutation_range.get(),
								optimizer=self.optimizer_entry.get(),
								statistics=self.statistics.get(), save=self.save.get(), plot=self.plot.get())

			if self.statistics.get():
				with open('results/GA-statistics.txt', 'r') as f:
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

		except Exception as err:
			print('Ошибка!\n', type(err))
			print(err)
			self.errorGUI()

	def errorGUI(self):
		self.root.destroy()
		root = Tk()
		root.title("ERROR")
		root.geometry('300x150+100+100')
		text = Text(width=20, height=3, font='arial 20', fg='red')
		text.insert(1.0, "\nЧТО-ТО ПОШЛО НЕ ТАК!")
		text.pack()
		ok_button = Button(text=" OK ", command=root.destroy, font='arial 17', 
								bg='red', state='active', bd=3, height=2, width=8)
		ok_button.pack()
		root.mainloop()





