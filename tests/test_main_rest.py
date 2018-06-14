import requests

if __name__ == "__main__":
    r = requests.post('http://localhost:8445/api',
                     data={
                         'MsgType': 'D',
                         'ClOrdID': 'abcd',
                         'Symbol': 'BTCUSD',
                         'Side': '2',
                         'OrdType': '2',
                         'Price': 5,
                         'OrderQty': 5,
                         'BrokerID': '5'
                     })
    # r = requests.get('http://localhost:8445/api/v1/BRL/ticker')