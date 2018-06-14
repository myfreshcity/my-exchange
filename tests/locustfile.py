import random
import string

from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        # self.client.post("/login", {"username":"ellen_key", "password":"education"})
        pass

    def logout(self):
        pass
        #self.client.post("/logout", {"username":"ellen_key", "password":"education"})




    @task(2)
    def index(self):
        self.client.get("/api/v1/BRL/ticker")


    @task(1)
    def profile(self):
        self.client.post("/",
                         data={
                             'MsgType': 'D',
                             'ClOrdID': 'abcd',
                             'Symbol': 'BTCUSD',
                             'Side': '2',
                             'OrdType': '2',
                             'Price': 5,
                             'OrderQty': 5,
                             'BrokerID': 5,
                         })
        #self.client.get("/api/v1/BRL/trades?since=2270000&limit=100")

class WebsiteUser(HttpLocust):
    host = "http://localhost:8445"
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000