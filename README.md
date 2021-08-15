# fsnd-capstone

## Udacity's Full Stack Developer Nanodegree Capstone Project

This project is currently a Flask API for a fashion store that sells all kinds of cool kid apparel. It's a work in progress but I'm hoping to further develop the API and create the front end for this.

[View the in progress app live here on Heroku.](https://skylight-fashion.herokuapp.com)

## Getting Started - Running the App Locally

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

Working within a virtual environment when using Python for projects keeps your dependencies separate and organized, therefore using a virtual environment is highly recommended. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once your virtual environment is setup and running, install dependencies for this project by running the following when in the project directory:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

### Running the server

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

The `FLASK_APP` environment variable specifies how to load the Flask application.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

Make sure to update any environment variables in `setup.sh` if necessary and run execute the command to export them to the environment:

```bash
source setup.sh
```

### Running Tests

You'll need two JWTs: one for each role listed in [roles](###Roles). After getting the two tokens, run:

```bash
python -m unittest test.py
```

## API Documentation

### Roles

- Customers
    - can only view the list of apparel items and post orders
    - has `get:items` and `post:orders` permissions

- Staff
    - can view list of apparel items, view all orders, post new apparel items, make updates to already posted apparel items, and delete items
    - has `get:items`, `get:orders`, `post:items`, `patch:items`, and `delete:items` permissions

### Endpoints

#### GET /apparel

Both customers and staff have access to this endpoint because of the `get:items` permission. Without proper permission, this will result in a `401` error. This endpoint gets the list of all apparel items available. Sample request:

`$ curl -X GET https://skylight-fashion.herokuapp.com/apparel`

#### GET /orders

Only staff have access to this endpoint because of the `get:orders` permission. Without proper permission, this will result in a `401` error. This endpoint gets the list of all orders in the database. Sample request:

`$ curl -X GET https://skylight-fashion.herokuapp.com/orders`

#### POST /apparel

Only staff have access to this endpoint because of the `post:items` permission. Without proper permission, this will result in a `401` error. If there are missing fields for the item, this will result in `422` error. This endpoint adds an apparel item to the database and returns the item that was just added. Sample request:

`$ curl -X POST https://skylight-fashion.herokuapp.com/apparel`

#### POST /orders

Only customers have access to this endpoint because of the `post:orders` permission. Without proper permission, this will result in a `401` error. If there are missing fields for the item, this will result in `422` error. This endpoint adds an order to the database and returns the order that was just added. Sample request:

`$ curl -X POST https://skylight-fashion.herokuapp.com/orders`

#### PATCH /apparel/{item_id}

Only staff have access to this endpoint because of the `patch:items` permission. Without proper permission, this will result in a `401` error. If the item id is not present in the database, this will result in a `404` error. If there are no fields for the item, this will result in `422` error. This endpoint updates an existing apparel item and returns the updated item. Sample request:

`$ curl -X PATCH https://skylight-fashion.herokuapp.com/apparel/1`

#### DELETE /apparel/{item_id}

Only staff have access to this endpoint because of the `delete:items` permission. Without proper permission, this will result in a `401` error. If the item id is not present in the database, this will result in a `404` error. This endpoint deletes an apparel item in the database and returns the id of the deleted item. Sample request:

`$ curl -X DELETE https://skylight-fashion.herokuapp.com/apparel/1`