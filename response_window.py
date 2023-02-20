
from tkinter import ttk
import intruder_functions as intruderClass
import tkinter as tk

class ResponseDetail:
    request_header = {}
    request_body = {}
    response_text = ""

    def __init__(self,request_header,request_body,response_text):
        self.request_header = request_header
        self.request_body = request_body
        self.response_text = response_text
    def __str__(self) -> str:
        return self.request_body["password"]


class Response_Window:
    response_window:tk.Tk
    list_box:tk.Listbox
    counter_label = ttk.Label
    response_list = list()
    index = 0
    def open_window_screen(self):
        self.response_window = tk.Tk()
        self.response_window.title("Response Windows")
        self.response_window.geometry("600x550")
        frame_1 = tk.Frame(self.response_window)  
        self.list_box = tk.Listbox(frame_1,width=60,height=30)
        self.list_box.pack(side = tk.LEFT, fill = tk.BOTH)
        scrollbar = tk.Scrollbar(frame_1)
        scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.list_box.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = self.list_box.yview)
        frame_1.grid(row=0,column=0)
        frame_2 = tk.Frame(self.response_window)
        self.counter_label = ttk.Label(self.response_window,text="Request Counter: 0")
        self.counter_label.grid(row=1,column=1)
        ttk.Button(frame_2,text="Show Details",command=self.showDetails).pack()
        frame_2.grid(row=0,column=1)
        self.response_window.mainloop()
    

    def draw_response(self,request_model,response_model):
        self.list_box.insert(self.index,f"Value: {request_model.request_param_value}            Length: {str(response_model.response_length)}")
        req_body = request_model.request_body.copy()
        req_header = request_model.requests_headers.copy()
        response_text = response_model.response_text
        response_model = ResponseDetail(req_header,req_body,response_text)
        self.response_list.insert(self.index,response_model)
        self.counter_label["text"] = f"Request Counter: {str(len(self.response_list))}"
        self.index = self.index + 1

    def showDetails(self): 
        index_number = self.list_box.curselection()[0]
        response_detail:ResponseDetail = self.response_list[index_number]
        detail_window = tk.Tk()
        detail_window.title("Detail Window")
        detail_window.geometry("800x700")
        request_text = tk.Text(
            detail_window,
            height=20,
            width=150,
        )
        response_text = tk.Text(
            detail_window,
            height=300,
            width=200
        )
        request_text.insert("end",f"Request Headers: {response_detail.request_header}\nRequest Body: {response_detail.request_body}")
        response_text.insert("end",f"{response_detail.response_text}")
        request_text.pack()
        response_text.pack()
        detail_window.mainloop()

