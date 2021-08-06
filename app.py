import os
from flask import Flask, request, abort
from flask_cors import CORS
from models import setup_db, ApparelItem
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
    GET /apparelitems:
        Public endpoint. Contains only the item.short() data representation.
        Returns status code 200 and the list of ApparelItems or appropriate
        status code indicating reason for failure.
    '''
    @app.route('/apparel', methods=['GET'])
    def get_apparel_items():
        all_apparel_items = ApparelItem.query.order_by(ApparelItem.item_name).all()

        return jsonify({
            'success': True,
            'apparel_items': [item.short() for item in all_apparel_items]
        }), 200

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()