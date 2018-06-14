import time
import random
# from socket import socket, AF_INET, SOCK_STREAM
import socket
from locust import Locust, TaskSet, events, task
from websocket import WebSocket


class TcpSocketClient(WebSocket):
    def __init__(self):
        super(TcpSocketClient, self).__init__()

    def connect(self, addr):
        start_time = time.time()
        try:
            super(TcpSocketClient, self).connect(addr)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcpsocket", name="connect", response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcpsocket", name="connect", response_time=total_time,
                                        response_length=0)

    def send(self, msg):
        start_time = time.time()
        try:
            super(TcpSocketClient, self).send(msg)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcpsocket", name="send", response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcpsocket", name="send", response_time=total_time,
                                        response_length=0)

    def recv(self, bufsize):
        recv_data = ''
        start_time = time.time()
        try:
            recv_data = super(TcpSocketClient, self).recv()
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcpsocket", name="recv", response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcpsocket", name="recv", response_time=total_time,
                                        response_length=0)
        return recv_data

class TcpSocketLocust(Locust):
    """ 
    This is the abstract Locust class which should be subclassed. It provides an TCP socket client 
    that can be used to make TCP socket requests that will be tracked in Locust's statistics. 
    """
    def __init__(self, *args, **kwargs):
        super(TcpSocketLocust, self).__init__(*args, **kwargs)
        self.client = TcpSocketClient()
        self.client.connect("ws://echo.websocket.org/")


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        pass
        #self.client.post("/login", {"username":"ellen_key", "password":"education"})

    def logout(self):
        pass
        #self.client.post("/logout", {"username":"ellen_key", "password":"education"})

    @task(1)
    def index(self):
        #self.client.send({ 'username': 'user', 'password': 'abc12345' ,'brokerId':5})
        self.client.send("Hello, World")
        data = self.client.recv(2048).decode()
        print(data)


class WebsiteUser(TcpSocketLocust):
    host = "ws://localhost:8445/"

    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000