from time import sleep
import alpaca_trade_api as alpaca
from django.http import JsonResponse
import requests
import json
from rest_framework import status

#ALPACA_API_BASE_URL = "https://paper-api.alpaca.markets"
#api_key = 'PK7N6TD62B2SRYC1YJJ6'
#secret_key = '3AWPZhEjvFSJJMKhB7qMQ1jSMirwdLtGL2VAOMpB'

#api = alpaca.REST(api_key, secret_key, ALPACA_API_BASE_URL, api_version='v2')
# for crypto qty
#account_info = api.get_position('LTCUSD').qty
#print(float(account_info))

#message = {"ticker": "LTCUSD","qty":1,
#            "side": "buy", "type": "market",
#            "time_in_force":"gtc", "limit_price":415,
#            "trail_price": 1, "bracket_stop_loss": 418,
#            "bracket_limit_price": 410, "bracket_take_profit": 430,
#            "stop_loss": 415, "stop_price": 410, "order_type": "simple_order"
#}

relevant_terms = ['ticker','qty','side','type','time_in_force',
                  'limit_price','stop_loss','bracket_stop_price',
                  'bracket_loss_limit','bracket_take_profit']

# crytpo is only compatible with simple,limit,and stop_price

class Order:
    
    def simple_order(message,api):
        api = api
        order = api.submit_order(
            symbol=message['ticker'],
            qty=message['qty'],
            side=message['side'],
            type='market',
            time_in_force=message['time_in_force'],
               )
        return json.dumps(order._raw)
    
    def limit_order(message,api):
         api = api
         order = api.submit_order(
            symbol=message['ticker'],
            qty=message['qty'],
            side=message['side'],
            type='limit',
            time_in_force=message['time_in_force'],
            limit_price=message['limit_price']
          )
         return json.dumps(order._raw)
         
    def stop_loss_order(message,api):
         api = api
         order = api.submit_order(
            symbol=message['ticker'],
            qty=message['qty'],
            side=message['side'],
            type='market',
            time_in_force=message['time_in_force'],
            order_class='oto',
            stop_loss={'stop_price': message['stop_loss']}
          )
         return json.dumps(order._raw)
    
    def bracket_order(message,api):
          api = api
          order = api.submit_order(
            symbol=message['ticker'],
            qty=message['qty'],
            side=message['side'],
            type='market',
            time_in_force=message['time_in_force'],
            order_class='bracket',
            stop_loss={'stop_price': message['bracket_stop_loss'],
               'limit_price':  message['bracket_limit_price']},
            take_profit={'limit_price': message['bracket_take_profit']}
          )
          return json.dumps(order._raw)

    def trailing_stop_order(message,api):
         api = api
         order = api.submit_order(
            symbol=message['ticker'],
            qty=message['qty'],
            side=message['side'],
            type='trailing_stop',
            trail_price=message['trail_price'],  # stop price will be hwm - 1.00$
            time_in_force=message['time_in_force'],
            )
         return json.dumps(order._raw)

    def stop_price_order(message,api):
        api = api
        order = api.submit_order(
                    symbol=message['ticker'],
                    qty=message['qty'],
                    side=message['side'],
                    type='stop_limit',
                    time_in_force=message['time_in_force'],
                    stop_price = message['stop_price'],
                    limit_price= message['limit_price']
                    )
        return json.dumps(order._raw)
        

order_classes = ['simple_order','limit_order','stop_loss_order',
                 'bracket_order','trailing_stop_order','stop_price_order']

def place_order(message,api):
     api=api
     if message['order_type'] == 'simple_order':
         order = Order.simple_order(message,api)

     elif message['order_type'] == 'limit_order':
        order =  Order.limit_order(message,api)
         
     elif message['order_type'] == 'stop_loss_order':
        order = Order.stop_loss_order(message,api)
     
     elif message['order_type'] == 'bracket_order':
        order=  Order.bracket_order(message,api)
        
     elif message['order_type'] == 'trailing_stop_order':
        order = Order.trailing_stop_order(message,api)
    
     elif message['order_type'] == 'stop_price_order':
        order = Order.stop_price_order(message,api)
     return order
       
     
     
     

