# fsnd-capstone

## Udacity's Full Stack Developer Nanodegree Capstone Project

This project is currently a Flask API for a fashion store that sells all kinds of cool kid apparel. It's a work in progress but I'm hoping to further develop the API and create the front end for this.

## Getting Started - Running the App Locally

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

Working within a virtual environment when using Python for projects keeps your dependencies separate and organized, therefore using a virtual environment is highly recommended. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once your virtual environment is setup and running, install dependencies for this project by running the following when in the project directory:

```bash
pip3 install -r requirements.txt
```
This will install all of the required packages within the `requirements.txt` file.

##### Key Dependencies

- [Flask](https://flask.palletsprojects.com/en/2.0.x/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Models are defined in `models.py` but routes and application logic are located in `app.py`.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Running the server

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

The `FLASK_APP` environment variable specifies how to load the Flask application.

To run the server locally, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

Make sure to update any environment variables in `setup.sh` if necessary and run execute the command to export them to the environment:

```bash
source setup.sh
```

### Running Tests

You'll need two JWTs: one for each role listed in [roles](###Roles). To generate them, follow the instructions in [Auth0 Set Up](###Auth0) to either replicate the Auth0 configuration for the project or use the test accounts. After getting the two tokens, run:

```bash
python -m unittest test.py
```

## API Documentation

### Auth0 Set Up

#### Creating Auth0 Application and API

1. Create a free acount at [Auth0](https://auth0.com/) if you don't already have one and log into that account.
2. Click on Applications Tab on the left and click "Applications" to load the next screen.
3. Click "Create Application" on the top right.
4. Pick "skylight" as the name for the application and select "Regular Web Applications". Click "Create" at the bottom right corner of the window.
5. Go to the Settings tab and find the "Domain" field. Copy and paste it to replace the value currently located in the `AUTH0_DOMAIN` field in `setup.sh`.
6. The "Client ID" will be used in [Generating Tokens](####Generating Tokens) so save it for later use.
7. Under "Application URIs", set "Application Login URI" to https://127.0.0.1:5000/login
8. Set "Allowed Callback URLs" to https://127.0.0.1:5000/login-results
9. Set "Allowed Logout URLs" to https://127.0.0.1:8100/logout and click "Save" at the bottom.
10. Under the Applications tab, click on "APIs".
11. Click "Create a new API" on the top right. Fill out the form with the following:
`Name: Skylight`
`Identifier: skylight`
Keep "Signing Algorithm" as is. The value for `ALGORITHMS` in `setup.sh` should match the one on the form. If not, copy and paste it there.
Replace the value currently located in the `API_AUDIENCE` field in `setup.sh` with "skylight".
12. Go to the "Settings" tab in the just newly created API, navigate to "RBAC Settings" and make sure the buttons for "Enable RBAC" and "Add Permissions in the Access Token" are green. Scroll down to the bottom and click "Save".

#### Setting up Roles and Permissions

1. Click the "API" tab under "Applications" and navigate to the Skylight API.
2. Click on Permissions and add the following permissions:
- get:items
- get:orders
- post:orders
- post:items
- patch:items
- delete:items
Feel free to put descriptions that are helpful for you.
3. Click "User Management" on the right, then click "Roles".
4. Click "Create Role" at the top right corner.
5. Enter "Customer" for the name, and a description of your choosing.
6. Repeat steps 3-5 for the "Staff" role.
7. Navigate to the Staff role. Click on the "Permissions" tab. Add the permissions for Staff specified under [roles](###Roles).
8. Repeat step 7 for the customer role but with the specified permissions.

#### Generating Tokens
If you created your own Auth0 set up, the url where you can make accounts is https://[YOUR AUTH0 DOMAIN HERE]/authorize?audience=skylight&response_type=token&client_id=[YOUR CLIENT ID HERE]redirect_uri=https://127.0.0.1:5000/login-results

You'll have to make two accounts: one for customer and one for staff. To assign roles after making the accounts, go to "User Management" > "Users". Click on the three dots at the right for the user you want to assign a role to and click "Assign Roles". After doing so, you can use the URL previously mentioned to generate JWTs for the logged in account.

There are two tests accounts to use if you did not set up your own API in Auth0:

- Staff 
    - email: aleg360@gmail.com
    - password: myqkih-sifxuz-6mAztu

- Customer
    - email: roselia.power@gmail.com
    - password: koghuj-9hivte-doxzAk

### Roles

- Customers
    - can only view the list of apparel items and post orders
    - has `get:items` and `post:orders` permissions

- Staff
    - can view list of apparel items, view all orders, post new apparel items, make updates to already posted apparel items, and delete items
    - has `get:items`, `get:orders`, `post:items`, `patch:items`, and `delete:items` permissions

### Endpoints

#### GET /apparel

Both customers and staff have access to this endpoint because of the `get:items` permission. Without proper permission, this will result in a `401` error. This endpoint gets the list of all apparel items available. Sample curl:

```bash
$ curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" https://skylight-fashion.herokuapp.com/apparel
```

Sample response:
```bash
{
    "apparel_items": [
        {
            "color": "beige",
            "id": 1,
            "item_name": "Hand Knitted Poncho",
            "price": 38,
            "released": "Tue, 15 Mar 2011 12:05:57 GMT",
            "target_demographic": "Women"
        }
    ],
    "success": true
}
```

#### GET /orders

Only staff have access to this endpoint because of the `get:orders` permission. Without proper permission, this will result in a `401` error. This endpoint gets the list of all orders in the database. Sample curl:

```bash
$ curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" https://skylight-fashion.herokuapp.com/orders
```

Sample response:
```bash
{
    "orders": [
        {
            "billing_city": "New York",
            "billing_state": "NY",
            "customer_name": "Alexa Rodriguez",
            "id": 1,
            "order_date": "Fri, 14 Feb 2020 09:05:57 GMT",
            "ship_city": "Pasadena",
            "ship_state": "CA",
            "user_id": null
        }
    ],
    "success": true
}
```

#### POST /apparel

Only staff have access to this endpoint because of the `post:items` permission. Without proper permission, this will result in a `401` error. If there are missing fields for the item, this will result in `422` error. This endpoint adds an apparel item to the database and returns the item that was just added. Sample curl:

```bash
curl https://skylight-fashion.herokuapp.com/apparel -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"item_name": "Long Sleeve Jersey Tee", "target_demographic": "Men", "color": "seaport blue", "price": 20,  "released": "2021-03-15 12:35:57.10558"}'
```

Sample response:
```bash
{
    "ApparelItem": [
        {
            "color": "seaport blue",
            "id": 2,
            "item_name": "Long Sleeve Jersey Tee",
            "price": 20,
            "released": "Mon, 15 Mar 2021 20:35:57 GMT",
            "target_demographic": "Men"
        }
    ],
    "success": true
}
```

#### POST /orders

Only customers have access to this endpoint because of the `post:orders` permission. Without proper permission, this will result in a `401` error. If there are missing fields for the item, this will result in `422` error. This endpoint adds an order to the database and returns the order that was just added. Sample curl:

`$ curl -X POST `
```bash
curl https://skylight-fashion.herokuapp.com/orders -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"customer_name": "Luke Field", "ship_city": "Madison", "ship_state": "WI", "billing_city": "Madison", "billing_state": "WI", "order_date": "2021-03-17 08:05:57.10558"}'
```

Sample response:

```bash
{
    "Order": [
        {
            "billing_city": "Madison",
            "billing_state": "WI",
            "customer_name": "Luke Field",
            "id": 2,
            "order_date": "Wed, 17 Mar 2021 08:05:57 GMT",
            "ship_city": "Madison",
            "ship_state": "WI",
            "user_id": null
        }
    ],
    "success": true
}
```

#### PATCH /apparel/{item_id}

Only staff have access to this endpoint because of the `patch:items` permission. Without proper permission, this will result in a `401` error. If the item id is not present in the database, this will result in a `404` error. If there are no fields for the item, this will result in `422` error. This endpoint updates an existing apparel item and returns the updated item. Sample curl:

`$ curl -X PATCH https://skylight-fashion.herokuapp.com/apparel/1`
```bash
curl https://skylight-fashion.herokuapp.com/apparel/2 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"item_name": "Long Sleeve Striped Jersey Tee", "price": 15}'
```

Sample response:
```bash
{
    "item": [
        {
            "color": "seaport blue",
            "id": 44,
            "item_name": "Long Sleeve Striped Jersey Tee",
            "price": 15,
            "released": "Mon, 15 Mar 2021 20:35:57 GMT",
            "target_demographic": "Men"
        }
    ],
    "success": true
}
```

#### DELETE /apparel/{item_id}

Only staff have access to this endpoint because of the `delete:items` permission. Without proper permission, this will result in a `401` error. If the item id is not present in the database, this will result in a `404` error. This endpoint deletes an apparel item in the database and returns the id of the deleted item. Sample curl:

```bash
curl https://skylight-fashion.herokuapp.com/apparel/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"
```

Sample response:
```bash
{
    "deleted": 44,
    "success": true
}
```

## Deployment

This app is currently deployed live [here on Heroku](https://skylight-fashion.herokuapp.com).