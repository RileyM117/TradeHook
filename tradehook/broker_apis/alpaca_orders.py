from time import sleep
import alpaca_trade_api as alpaca
from django.http import JsonResponse
import requests
import json
import math
from rest_framework import status

relevant_terms = ['ticker','qty','side','type','time_in_force',
                  'limit_price','stop_loss','bracket_stop_price',
                  'bracket_loss_limit','bracket_take_profit']

# crytpo is only compatible with simple,limit,and stop_price

# Defining different types of orders under one class

class Order:
    # Order to simply buy and or sell assets
    def simple_order(message,api):
        api = api
        order = api.submit_order(
            symbol=message['ticker'],
            qty=message['qty'],
            side=message['side'],
            type='market',
            time_in_force=message['time_in_force'],
               )
        # Instead of returning entire raw order response, return only relevant info.
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
    
    # crypto orders require different methods to automate selling due to fees
    def crypto_simple_sell(message,api):
        api = api
        # Math to calc fees. This is necessary because fee rates on crypto change.
        # get the open order quantity of the provided symbol. If buy quantity = 1, this quantity will be something like 0.9975
        order_qty = float(api.get_position(message['ticker']).qty) 
        # calculate the qty minus fees. Example: if buy quantity = 2, order_qty = 1.995. order_qty_mod = 1.995 / 2  = 0.9975
        order_qty_mod = order_qty / math.ceil(order_qty) 
        # round to 4 decimal four sig figs. 
        order_qty_mod_final = round(order_qty_mod,4)
        # calculate actual quantity to sell based on provided qty by multiplying by 1 - fee. Also round to 4 sig figs
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
    
    def sell_all(message,api):
         api=api
         qty = int(api.get_position(message['ticker']).qty)
         order = api.submit_order(
          symbol=message['ticker'],
          qty=qty,
          side=message['side'],
          type='market',
          time_in_force='gtc'  # Good 'til Cancelled
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
    
    def crypto_sell_all(message,api):
         api=api
         order_qty = float(api.get_position(message['ticker']).qty)
         order = api.submit_order(
          symbol=message['ticker'],
          qty=order_qty,
          side=message['side'],
          type='market',
          time_in_force='gtc'  # Good 'til Cancelled
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

     elif message['order_type'] == 'sell_all':
        order = Order.sell_all(message,api)
      
     elif message['order_type'] == 'crypto_sell_all':
        order = Order.crypto_sell_all(message,api)



     return order
       
     
     
     

