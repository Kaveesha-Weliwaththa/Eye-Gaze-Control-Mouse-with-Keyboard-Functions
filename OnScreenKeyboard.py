from tkinter import *
import tkinter

keyboard = tkinter.Tk()
keyboard.title("Virtual Keyboard")
keyboard.config(bg="yellow")
#keyboard.wm_iconbitmap("math.ico")
keyboard.resizable(0, 0)


def select(value):
    if value == "Space":
        entry.insert(INSERT, ' ')

    elif value == "Tab":
        entry.insert(INSERT, '     ')

    elif value == "Enter":
        entry.insert(INSERT, '\n')

    elif value == "Delete":
        entry.delete(1.0, END)

    else:
        entry.insert(INSERT, value)

name = Label(keyboard, text="Virtual Keyboard", font=("arial", 20, "bold"), bg="yellow", fg="black")
name.grid(row=0, columnspan=40)

entry = Text(keyboard, width=202, font=("arial", 10, "bold"), wrap=WORD)
entry.grid(row=1, columnspan=40)

key_board = ['~',         '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Delete', '7', '8', '9', '/',
            'Tab',       'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[',          '4', '5', '6', '*',
            'Caps Lock', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', 'Enter',      '1', '2', '3', '-',
            'Shift',     'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', ']',          '(', '0', ')', '+',
            'Space']

varRow = 2
varColumn = 0

for key in key_board:
    command = lambda x=key: select(x)
    if key != "Space":
        other = tkinter.Button(keyboard, text=key, width=5, activebackground="black", bg='black', fg="white", activeforeground="yellow", padx=3, pady=3, bd=12, font=('arial', 15, 'bold'), command=command)
        other.grid(row=varRow, column=varColumn)

    if key == "Space":
        space = tkinter.Button(keyboard, text=key, activebackground="black", bg='black', fg="white", activeforeground="yellow", width=110, padx=3, pady=3, bd=12, font=('arial', 15, 'bold'), command=command)
        space.grid(row=7, columnspan=40)

    varColumn += 1
    if varColumn > 15 and varRow == 2:
        varColumn = 0
        varRow += 1
    if varColumn > 15 and varRow == 3:
        varColumn = 0
        varRow += 1
    if varColumn > 15 and varRow == 4:
        varColumn = 0
        varRow += 1
    if varColumn > 15 and varRow == 5:
        varColumn = 0
        varRow += 1

keyboard.mainloop()


