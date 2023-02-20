import tkinter
from tkinter import ttk
import intruder_functions as inf
import threading
from tkinter import filedialog as fd
#from tkinter.messagebox import showinfo

class Intruder:
    header_data:dict
    body_data:dict
    url:tkinter.StringVar
    fuzz_param:tkinter.StringVar
    fuzz_list:str
    request_type:tkinter.StringVar
    window:tkinter.Tk
    fuzz_file:str
    header_key_list = list()
    header_data_list = list()
    body_key_list = list()
    body_data_list = list()

    def createHeaderSection(self,window):
        key_entry_val = tkinter.StringVar()
        data_entry_val = tkinter.StringVar()

        new_header_frame = tkinter.Frame(window)
        header_label = ttk.Label(new_header_frame,text="Header " + str(len(self.header_data_list) + 1))
        key_entry = ttk.Entry(new_header_frame,textvariable=key_entry_val)
        key_data = ttk.Entry(new_header_frame,textvariable=data_entry_val)

        header_label.grid(row=0,column=0)
        key_entry.grid(row=0,column=1)
        ttk.Label(new_header_frame,text=":").grid(row=0,column=2)
        key_data.grid(row=0,column=3)
        new_header_frame.pack()
        return (key_entry_val,data_entry_val)
    
    def add_header(self,window):
        header_key_data = self.createHeaderSection(window)
        self.header_key_list.append(header_key_data[0])
        self.header_data_list.append(header_key_data[1])

    def createBodySection(self,window):
        key_entry_val = tkinter.StringVar()
        data_entry_val = tkinter.StringVar()

        new_body_frame = tkinter.Frame(window)
        header_label = ttk.Label(new_body_frame,text="Body " + str(len(self.body_data_list) + 1))
        key_entry = ttk.Entry(new_body_frame,textvariable=key_entry_val)
        key_data = ttk.Entry(new_body_frame,textvariable=data_entry_val)

        header_label.grid(row=0,column=0)
        key_entry.grid(row=0,column=1)
        ttk.Label(new_body_frame,text=":").grid(row=0,column=2)
        key_data.grid(row=0,column=3)
        new_body_frame.pack()
        return (key_entry_val,data_entry_val)
    
    def add_body_data(self,window):
        body_key_data = self.createBodySection(window)
        self.body_key_list.append(body_key_data[0])
        self.body_data_list.append(body_key_data[1])

    def getParams(self,param_type):
        values = list()
        if param_type == "Header":
            for val in self.header_key_list:
                values.append(val.get())
        elif param_type == "Body":
            for val in self.body_key_list:
                values.append(val.get())
        return tuple(values)
    def startAttack(self,request_thread:inf.RequestThread):
        request_thread.url = self.url.get()
        request_thread.request_type = self.request_type.get()
        dict_body = {}
        dict_header = {}
        for i in range(len(self.body_key_list)):
            dict_body[self.body_key_list[i].get()] = self.body_data_list[i].get()
        for i in range(len(self.header_key_list)):
            dict_header[self.header_key_list[i].get()] = self.header_data_list[i].get()
        request_thread.brute_dict_body = dict_body
        request_thread.brute_dict_header = dict_header
        request_thread.brute_param = self.fuzz_param.get()
        request_thread.brute_file = self.fuzz_file
        print(f"Header:{dict_header}\nBody:{dict_body}\nUrl:{self.url.get()}\nBrute Param:{self.fuzz_param.get()}")
        request_thread.thread_speed = 10
        threading.Thread(target=request_thread.start_thread).start()
        #request_thread.start_thread()
    def selectFile(self,showinfo):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        self.fuzz_file = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        
        showinfo(
            title='Selected File',
            message=self.fuzz_file
        )
