import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

'''
This api is just for the tests runner for postman ,
to make sure tests are not flaky.it requires manager permission
'''
@app.route('/clearall', methods=['GET'])
@requires_auth('patch:drinks')
@requires_auth('post:drinks')
@requires_auth('delete:drinks')
def clear_all(a, b, c):
    db_drop_and_create_all()
    return jsonify({"success": True, "message": "all db cleared"})


# ROUTES
'''
implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and
    json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def getDrinks():
    drinks = Drink.query.order_by(Drink.id).all()
    drinks_formated = [drink.short() for drink in drinks]
    return jsonify({"success": True, "drinks": drinks_formated})


'''
implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200
    and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def getDrinkDetail(jwt):
    drinks = Drink.query.order_by(Drink.id).all()
    drinks_formated = [drink.long() for drink in drinks]
    return jsonify({"success": True, "drinks": drinks_formated})


'''
implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200
    and json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def postDrink(jwt):
    body = request.get_json()

    try:
        title = body.get('title', None)
        recipe = body.get('recipe', {})

        drinks = Drink.query.filter(Drink.title.like(title)).count()
        print("current", drinks)
        if drinks > 0:
            raise AuthError({
                'code': 'Bad request',
                'description': "This drink is already existent"
            }, 400)
        drink = Drink(
            title=title, recipe=f"""
            [{json.dumps(recipe, separators=(',', ':'))}]
            """)
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception as e:
        print("exception error post drink", e)
        print(e)
        if isinstance(e, AuthError):
            raise e
        abort(406)


'''
implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200
    and json {"success": True, "drinks": drink}
    where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def updateDrinks(jwt, id):
    body = request.get_json()

    title = body.get('title', None)
    recipe = body.get('recipe', None)
    try:
        drink = Drink.query.get(id)

        if drink is None:
            abort(404)

        if title is not None:
            drink.title = title
        if recipe is not None:
            drink.recipe = json.dumps(recipe,  separators=(',', ':'))
        drink.update()

        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })
    except Exception as exc:
        print(exc)
        abort(404)


'''
implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200
    and json {"success": True, "delete": id}
    where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def deleteDrinks(jwt, id):

    try:
        drink = Drink.query.get(id)

        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
            "success": True,
            "drink": drink.id
        })
    except Exception as exc:
        print(exc)
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using
the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def handleError404(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(406)
def handleError406(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 406,
        "message": "Could not create new resouce"
    }), 406


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def handleAuthError(error):
    print("auth erorr", error)
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), 401
