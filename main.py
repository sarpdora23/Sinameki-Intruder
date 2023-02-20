import requests
import ui_functions as uif
import intruder_functions as inf
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo



class Spacer:
    def __init__(self,window,width,height):
        text = ""
        for i in range(width):
            text = text + " "
        for i in range(height -1):
            text = text + "\n"
        ttk.Label(window,text=text).pack()
def setParameter(event,intruder,combobox):
    print("Test")
    combobox["values"] = intruder.getParams(fuzz_param_type.get())


window = tk.Tk()
window.title("Sinameki Intruder")
window.geometry("800x600")
window.resizable(False,False)
window.iconbitmap("./sinameki_intruder_icon.ico")

intruder = uif.Intruder()
request_thread = inf.RequestThread()
intruder.request_type = tk.StringVar()
intruder.fuzz_param = tk.StringVar()

url_val = tk.StringVar()
intruder.url = url_val

url_frame = tk.Frame(window)
url_label = ttk.Label(url_frame,text="Url:")
request_type = ttk.Label(url_frame,text="Request Type:")
type_combo_box = ttk.Combobox(url_frame,textvariable=intruder.request_type,state="readonly")
type_combo_box["values"] = (
    '',
    'GET',
    'POST'
)
url_entry = ttk.Entry(url_frame,textvariable=url_val)

headers_frame = tk.Frame(window)
add_header_button = ttk.Button(window,text="Add Header",command= lambda: intruder.add_header(headers_frame))

body_data_frame = tk.Frame(window)
add_body_button = ttk.Button(window,text="Add Parameter",command=lambda:intruder.add_body_data(body_data_frame))

attack_frame = tk.Frame(window)
ttk.Label(attack_frame,text="Select Fuzzing Parameter:").grid(row=0,column=0)
fuzz_param_type = tk.StringVar()

type_values=ttk.Combobox(attack_frame,textvariable=fuzz_param_type,state="readonly",values=("","Header","Body"))
param_values=ttk.Combobox(attack_frame,textvariable=intruder.fuzz_param,state="readonly",values=intruder.getParams(fuzz_param_type.get()))
type_values.grid(row=0,column=1)
param_values.grid(row=0,column=2)
sf_label = ttk.Label(attack_frame,text="Select File:")
sf_label.grid(row=0,column=3)
file_icon = tk.PhotoImage(file="./document.png",height=30,width=30)
ttk.Button(attack_frame,image=file_icon,command= lambda: intruder.selectFile(showinfo)).grid(row=0,column=5)
#type_values.bind("<<ComboboxSelected>>",lambda:setParameter(intruder=intruder,combobox=param_values))
type_values.bind("<<ComboboxSelected>>",lambda e:setParameter(event=e,intruder=intruder,combobox=param_values))

tk.Label(window,text="Sinameki Intruder",font=('Helvetica', 16)).pack()
Spacer(window,0,1)
tk.Label(window,text="General Options",font=('Helvetica', 12)).pack()
url_label.grid(row=0,column=0)
url_entry.grid(row=0,column=1)
request_type.grid(row=1,column=0)
type_combo_box.grid(row=1,column=1)
url_frame.pack()
Spacer(window,0,1)
tk.Label(window,text="Headers Data",font=('Helvetica', 12)).pack()
headers_frame.pack()
add_header_button.pack()
Spacer(window,0,1)
tk.Label(window,text="Body Data",font=('Helvetica', 12)).pack()
body_data_frame.pack()
add_body_button.pack()
Spacer(window,0,1)
attack_frame.pack()
ttk.Button(window,text="Attack",command=lambda:intruder.startAttack(request_thread=request_thread)).pack()
window.mainloop()