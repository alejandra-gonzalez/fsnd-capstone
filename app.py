import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, ApparelItem, Order, OrderItem
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

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
            'apparel_items': [item.format() for item in all_apparel_items]
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
        all_orders = [order.format() for order in Order.query.all()]

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
        if ('item_name' not in req or 'target_demographic' not in req or
        'price' not in req or 'color' not in req or 'released' not in req):
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
        if ('customer_name' not in req or 'ship_city' not in req or 
        'ship_state' not in req or 'billing_city' not in req or 'billing_state'
        not in req or 'order_date' not in req):
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

    '''
    PATCH /apparel/<id>
        where <id> is the existing ApparelItem id:
        Responds with a 404 error if <id> is not found. Updates the 
        corresponding row for <id>. Requires the 'patch:items' permission. 
        Returns status code 200 and an array with the updated ApparelItem or
        the appropriate status code indicating reason for failure.
    '''
    @app.route('/apparel/<int:id>', methods=['PATCH'])
    @requires_auth('patch:items')
    def update_item(jwt, id):
        item = ApparelItem.query.get(id)
        if item is None:
            abort(404)
        
        req = request.get_json()
        if not bool(req):
            abort(422)
        if 'item_name' in req:
            item.item_name = req['item_name']
        if 'target_demographic' in req:
            item.target_demographic = req['target_demographic']
        if 'price' in req:
            item.price = req['price']
        if 'color' in req:
            item.color = req['color']
        if 'released' in req:
            item.released = req['released']
        item.update()
        
        return jsonify({
            'success': True,
            'item': [item.format()]
        }), 200

    '''
    DELETE /apparel/<id>
            Where <id> is the existing ApparelItem id:
            Responds with a 404 error if <id> is not found. Deletes the 
            corresponding row for <id>. Requires the 'delete:items' permission.
            Returns status code 200 and the id of the deleted ApparelItem or
            the appropriate status code indicating reason for failure.
    '''
    @app.route('/apparel/<int:id>', methods=['DELETE'])
    @requires_auth('delete:items')
    def delete_item(jwt, id):
        item = ApparelItem.query.get(id)
        if item is None:
            abort(404)
        item.delete()

        return jsonify({
            'success': True,
            'deleted': item.id
        }), 200

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()