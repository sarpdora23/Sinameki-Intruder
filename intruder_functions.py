import requests
import threading
import time
import response_window
from response_window import Response_Window
class RequestModel:
    request_type = ""
    requests_headers = {}
    request_body = {}
    request_json = {}
    request_url = ""
    request_param = ""
    request_param_value = ""
    def __init__(self,request_type,request_headers,request_body,request_json,request_url,request_param,request_param_value):
        self.request_body = request_body
        self.request_json = request_json
        self.request_type = request_type
        self.request_url = request_url
        self.requests_headers = request_headers
        self.request_param = request_param
        self.request_param_value = request_param_value
class ResponseRequest:
    request:RequestModel
    response_length:int
    response_text = ""
    response_time = 0
    def __init__(self,request,response_length,response_text,response_time):
        self.request = request
        self.response_length = response_length
        self.response_text = response_text
        self.response_time = response_time
class RequestThread:
    url:str
    response_list = []
    brute_dict_header:dict
    brute_dict_body:dict
    brute_file:str
    brute_param:str
    thread_speed:int
    request_type:str
    
    def send_request(self,brute_val,param_flag,response_window:Response_Window):
        response_model:ResponseRequest
        request_type = self.request_type
        if param_flag == "body":
            self.brute_dict_body[self.brute_param] = brute_val
        elif param_flag == "header":
            self.brute_dict_header[self.brute_param] = brute_val
        header = self.brute_dict_header
        body = self.brute_dict_body
        json = {}
        print("Body:",body)
        url = self.url
        if request_type == "GET":
            request_model = RequestModel(request_type,header,body,json,url,self.brute_param,brute_val)
            response = requests.get(url,params=body,headers=header)
            response_model = ResponseRequest(request=request_model,response_length=len(response.text),response_text=response.text,response_time=0)
            response_window.draw_response(request_model,response_model)
           # print("Request:" +  body[self.brute_param] + " Length:" + str(response_model.response_length) + "\n")
        elif request_type == "POST":
            request_model = RequestModel(request_type,header,body,json,url,self.brute_param,brute_val)
            response = requests.post(url,data=body,headers=header,json=json)
            response_model = ResponseRequest(request=request_model,response_length=len(response.text),response_text=response.text,response_time=0)
            response_window.draw_response(request_model,response_model)
            #print("Request:" +  body[self.brute_param] + " Length:" + str(response_model.response_length) + "\n")
        return response_model
    
    def createNumberThread(self,wordlist,param_flag,response):
        thread_list = []
        body_data = {}
        header_data = {}
        for brute_value in wordlist:
            if param_flag == "body":
                body_data[self.brute_param] = brute_value
            elif param_flag == "header":
                header_data[self.brute_param] = brute_value
            one_thread = threading.Thread(target=self.send_request,args=(brute_value,param_flag,response))
            one_thread.start()
            time.sleep(0.2)
            thread_list.append(one_thread)
        for thread in thread_list:
            thread.join()
    def start_thread(self):
        response_window = Response_Window()
        threading.Thread(target=response_window.open_window_screen).start()
        attack_file = open(self.brute_file,"r")
        index = 0
        word_list = attack_file.read().split("\n")
        param_flag = ""
        if self.brute_param in self.brute_dict_body.keys():
            param_flag = "body"
        elif self.brute_param in self.brute_dict_header.keys():
            param_flag = "header" 
        for num in range(1,((len(word_list) // self.thread_speed) + 2)):
            if (num * self.thread_speed) < len(word_list):
                print("Less")
                self.createNumberThread(word_list[index: (num * self.thread_speed)],param_flag,response_window)
                index += self.thread_speed
            else:
                print("Bigger")
                self.createNumberThread(word_list[index:],param_flag,response_window)
           
        attack_file.close()



