import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, ApparelItem, Order
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    # ROUTES
    '''
    GET /apparel:
        Requires the 'get:items' permission. Contains the item.short() data
        representation. Returns status code 200 and the list of ApparelItems
        or appropriate status code indicating reason for failure.
    '''
    @app.route('/apparel', methods=['GET'])
    @requires_auth('get:items')
    def get_apparel_items(jwt):
        all_apparel_items = ApparelItem.query.order_by(ApparelItem.item_name).all()

        return jsonify({
            'success': True,
            'apparel_items': [item.short() for item in all_apparel_items]
        }), 200

    '''
    GET /orders:
        Requires the 'get:orders' permission. Contain the order.short() data
        representation. Returns status code 200 and the list of Orders or the
        appropriate status code indicating reason for failure.
    '''
    @app.route('/orders', methods=['GET'])
    @requires_auth('get:orders')
    def get_orders(jwt):
        all_orders = [order.short() for order in Order.query.all()]

        return jsonify({
            'success': True,
            'orders': all_orders
        }), 200

    '''
    POST /apparel:
        Requires the 'post:items' permission. Creates a new row in the
        ApparelItems table. Returns status code 200 and an array with the new
        ApparelItem or the appropriate status code indicating reason for
        failure.
    '''
    @app.route('/apparel', methods=['POST'])
    @requires_auth('post:items')
    def post_item(jwt):
        req = request.get_json()
        if ('item_name' and 'target_demographic' and 'price' and 'color' and 
        'released' not in req):
            abort(422)
        
        item_name = req['item_name']
        target_demographic = req['target_demographic']
        price = req['price']
        color = req['color']
        released = req['released']
        item = ApparelItem(item_name=item_name, 
            target_demographic=target_demographic, price=price, color=color, 
            released=released)
        item.insert()

        return jsonify({
            'success': True,
            'ApparelItem': [item.format()]
        }), 200

    '''
    POST /orders:
        Requires the 'post:orders' permission. Creates a new row in the Orders
        table. Returns status code 200 and an array with the new Order or the
        appropriate status code indicating reason for failure.
    '''
    @app.route('/orders', methods=['POST'])
    @requires_auth('post:orders')
    def post_order(jwt):
        req = request.get_json()
        if ('customer_name' and 'ship_city' and 'ship_state' and 'billing_city' and 'billing_state' and 'order_date' not in req):
            abort(422)
        
        customer_name = req['customer_name']
        ship_city = req['ship_city']
        ship_state = req['ship_state']
        billing_city = req['billing_city']
        billing_state = req['billing_state']
        order_date = req['order_date']
        order = Order(customer_name=customer_name, ship_city=ship_city, 
        ship_state=ship_state, billing_city=billing_city, 
        billing_state=billing_state, order_date=order_date, user_id=None)

        order.insert()

        return jsonify({
            'success': True,
            'Order': [order.format()]
        }), 200

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()