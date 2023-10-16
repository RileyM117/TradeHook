from time import sleep
import alpaca_trade_api as alpaca
from django.http import JsonResponse
import requests
import json
import math
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
        order_id = order._raw['id']
        order_client_order_id= order._raw['client_order_id']
        order_symbol = order._raw['symbol']
        order_asset_class = order._raw['asset_class']
        order_qty = order._raw['qty']
        order_type = order._raw['order_type']
        order_side = order._raw['side']
        order_time_in_force = order._raw['time_in_force']
        return json.dumps({"id": order_id,"client order id": order_client_order_id,
                           "order symbol": order_symbol,"order asset class": order_asset_class,
                           "order quantity": order_qty,"order type": order_type,
                           "order side": order_side,"time in force": order_time_in_force})
        #return json.dumps(order._raw['id'])
    
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
         order_id = order._raw['id']
         order_client_order_id= order._raw['client_order_id']
         order_symbol = order._raw['symbol']
         order_asset_class = order._raw['asset_class']
         order_qty = order._raw['qty']
         order_limit_price = order._raw['limit_price']
         order_type = order._raw['order_type']
         order_side = order._raw['side']
         order_time_in_force = order._raw['time_in_force']
         return json.dumps({"id": order_id,"client order id": order_client_order_id,
                           "order symbol": order_symbol,"order asset class": order_asset_class,
                           "order quantity": order_qty,"limit price": order_limit_price,"order type": order_type,
                           "order side": order_side,"time in force": order_time_in_force})
         #return json.dumps(order._raw)
         
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
          #return json.dumps(order._raw)
         order_id = order._raw['id']
         order_client_order_id= order._raw['client_order_id']
         order_symbol = order._raw['symbol']
         order_asset_class = order._raw['asset_class']
         order_qty = order._raw['qty']
         order_type = order._raw['order_type']
         order_side = order._raw['side']
         order_time_in_force = order._raw['time_in_force']
         return json.dumps({"id": order_id,"client order id": order_client_order_id,
                           "order symbol": order_symbol,"order asset class": order_asset_class,
                           "order quantity": order_qty,"order type": order_type,
                           "order side": order_side,"time in force": order_time_in_force})
    
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
          order_id = order._raw['id']
          order_client_order_id= order._raw['client_order_id']
          order_symbol = order._raw['symbol']
          order_asset_class = order._raw['asset_class']
          order_qty = order._raw['qty']
          order_class = order._raw['order_class']
          order_type = order._raw['order_type']
          order_side = order._raw['side']
          order_time_in_force = order._raw['time_in_force']
          return json.dumps({"id": order_id,"client order id": order_client_order_id,
                           "order symbol": order_symbol,"order asset class": order_asset_class,
                           "order quantity": order_qty,"order type": order_type, "order class": order_class,
                           "order side": order_side,"time in force": order_time_in_force})
          

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
         order_id = order._raw['id']
         order_client_order_id= order._raw['client_order_id']
         order_symbol = order._raw['symbol']
         order_asset_class = order._raw['asset_class']
         order_qty = order._raw['qty']
         order_trail_price = order._raw['trail_price']
         order_type = order._raw['order_type']
         order_side = order._raw['side']
         order_time_in_force = order._raw['time_in_force']
         return json.dumps({"id": order_id,"client order id": order_client_order_id,
                           "order symbol": order_symbol,"order asset class": order_asset_class,
                           "order quantity": order_qty,"order type": order_type,
                           "trail price": order_trail_price,
                           "order side": order_side,"time in force": order_time_in_force})
         #return json.dumps(order._raw)

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
        
        order_id = order._raw['id']
        order_client_order_id= order._raw['client_order_id']
        order_symbol = order._raw['symbol']
        order_asset_class = order._raw['asset_class']
        order_qty = order._raw['qty']
        order_stop_price = order._raw['stop_price']
        order_limit_price = order._raw['limit_price']
        order_type = order._raw['order_type']
        order_side = order._raw['side']
        order_time_in_force = order._raw['time_in_force']
        return json.dumps({"id": order_id,"client order id": order_client_order_id,
                           "order symbol": order_symbol,"order asset class": order_asset_class,
                           "order quantity": order_qty,"order type": order_type,
                           "stop price": order_stop_price,"limit price": order_limit_price,
                           "order side": order_side,"time in force": order_time_in_force})
        
    def crypto_simple_sell(message,api):
        api = api
        order_qty = float(api.get_position(message['ticker']).qty)
        order_qty_mod = order_qty /math.ceil(order_qty)
        order_qty_mod_final = round(order_qty_mod,4)
        qty = round(message['qty'] * order_qty_mod_final,4)
        order = api.submit_order(
            symbol=message['ticker'],
            qty=qty,
            side='sell',
            type='market',
            time_in_force=message['time_in_force'],
               )
        order_id = order._raw['id']
        order_client_order_id= order._raw['client_order_id']
        order_symbol = order._raw['symbol']
        order_asset_class = order._raw['asset_class']
        order_qty = order._raw['qty']
        order_type = order._raw['order_type']
        order_side = order._raw['side']
        order_time_in_force = order._raw['time_in_force']
        return json.dumps({"id": order_id,"client order id": order_client_order_id,
                           "order symbol": order_symbol,"order asset class": order_asset_class,
                           "order quantity": order_qty,"order type": order_type,
                           "order side": order_side,"time in force": order_time_in_force})
    
    def crypto_limit_sell(message,api):
         api = api
         order_qty = float(api.get_position(message['ticker']).qty)
         order_qty_mod = order_qty /math.ceil(order_qty)
         order_qty_mod_final = round(order_qty_mod,4)
         qty = round(message['qty'] * order_qty_mod_final,4)
         order = api.submit_order(
            symbol=message['ticker'],
            qty=qty,
            side='sell',
            type='limit',
            time_in_force=message['time_in_force'],
            limit_price=message['limit_price']
          )
         order_id = order._raw['id']
         order_client_order_id= order._raw['client_order_id']
         order_symbol = order._raw['symbol']
         order_asset_class = order._raw['asset_class']
         order_qty = order._raw['qty']
         order_limit_price = order._raw['limit_price']
         order_type = order._raw['order_type']
         order_side = order._raw['side']
         order_time_in_force = order._raw['time_in_force']
         return json.dumps({"id": order_id,"client order id": order_client_order_id,
                           "order symbol": order_symbol,"order asset class": order_asset_class,
                           "order quantity": order_qty,"limit price": order_limit_price,"order type": order_type,
                           "order side": order_side,"time in force": order_time_in_force}) 

    def crypto_stop_price_sell(message,api):
        api = api
        order_qty = float(api.get_position(message['ticker']).qty)
        order_qty_mod = order_qty /math.ceil(order_qty)
        order_qty_mod_final = round(order_qty_mod,4)
        qty = round(message['qty'] * order_qty_mod_final,4)
        order = api.submit_order(
                    symbol=message['ticker'],
                    qty=qty,
                    side='sell',
                    type='stop_limit',
                    time_in_force=message['time_in_force'],
                    stop_price = message['stop_price'],
                    limit_price= message['limit_price']
                    )
        
        order_id = order._raw['id']
        order_client_order_id= order._raw['client_order_id']
        order_symbol = order._raw['symbol']
        order_asset_class = order._raw['asset_class']
        order_qty = order._raw['qty']
        order_stop_price = order._raw['stop_price']
        order_limit_price = order._raw['limit_price']
        order_type = order._raw['order_type']
        order_side = order._raw['side']
        order_time_in_force = order._raw['time_in_force']
        return json.dumps({"id": order_id,"client order id": order_client_order_id,
                           "order symbol": order_symbol,"order asset class": order_asset_class,
                           "order quantity": order_qty,"order type": order_type,
                           "stop price": order_stop_price,"limit price": order_limit_price,
                           "order side": order_side,"time in force": order_time_in_force})

order_classes = ['simple_order','limit_order','stop_loss_order',
                 'bracket_order','trailing_stop_order','stop_price_order','crypto_simple_sell',
                 'crypto_limit_sell','crypto_stop_price_sell']

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

     elif message['order_type'] == 'crypto_simple_sell':
        order = Order.crypto_simple_sell(message,api)

     elif message['order_type'] == 'crypto_limit_sell':
        order = Order.crypto_limit_sell(message,api)
      
     elif message['order_type'] == 'crypto_stop_price_sell':
        order = Order.crypto_stop_price_sell(message,api)

     return order
       
     
     
     

