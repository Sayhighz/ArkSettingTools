import tkinter as tk

def toggle_state():
    if checkbutton['state'] == tk.NORMAL:
        checkbutton['state'] = tk.DISABLED
    else:
        checkbutton['state'] = tk.NORMAL

root = tk.Tk()

checkbutton = tk.Checkbutton(root, text="Click me")
checkbutton.pack()

toggle_button = tk.Button(root, text="Toggle State", command=toggle_state)
toggle_button.pack()

root.mainloop()
