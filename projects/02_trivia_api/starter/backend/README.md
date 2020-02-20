# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


#Endpoints

```
GET '/categories'
GET '/questions'
POST '/questions'
DELETE '/questions/<int: question_id>'
GET '/questions/search'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a paginated questions 
- Request Arguments: None
- Returns: An array of question objects where each object contains of id: uniqe to each question, question: question_string, answer: answer_string, difficulty: difficulty_int , category:category_int represent the category it belongs to 
[{
    id: 1,
    question: "what is  the name of jordan king",
    answer: "King abdullah the second",
    category: 99,
    difficulty: 1
}]
- errors: return 404 in case of no questions available or no categories found


DELETE '/questions/<int: question_id>'
- Delete certain question based on an id
- Request Arguments: question_id as query parameter
- Returns: an object with a success set to true or false and a success message
{
    success: True,
    message: "message has been deleted successfully"
}


POST '/questions'
- Create New Question 
- Request Arguments: Body->JSON difficulty: question difictuly form 1 to 5, question: question string, answer: answer string, category: category id that this question belongs to
- Returns: An Object contains success:Boolean, created:question id as int, questions: array of current question objects,total_questions: number of total questions after creation
[{
    success: 1,
    questions: [<Question>],
    total_questions: 12,
    created: 12
}]

- errors: 422 in case we could not create new question

POST '/questions/search'
- Search for questions based on searchTerm
- Request Arguments: searchTerm: as string
- Returns: an Array of found Questions Objects
{
    success: True,
        questions: [{
        id: 1,
        question: "what is  the name of jordan king",
        answer: "King abdullah the second",
        category: 99,
        difficulty: 1
    }]
}


GET '/categories/<int:category_id>/questions'
- Fetches questions based on certain category
- Request Arguments: category_id as query param
- Returns: An array of question objects
{
    success: True,
    questions: [{
        id: 1,
        question: "what is  the name of jordan king",
        answer: "King abdullah the second",
        category: 99,
        difficulty: 1
    }]
}


POST '/quizzes'
- Find the next question based on category and previous asked questions
- Request Arguments: previous_questions: as array of questions ids, quiz_category: as Category object
- Returns: an Object representing if request is success and next question if available otherwise the question will be None
{
    success: True,
    question: {
        id: 1,
        question: "what is  the name of jordan king",
        answer: "King abdullah the second",
        category: 99,
        difficulty: 1
    }
}

- erros: 500 for internal server error
```


# running the Front End 

```
cd  frontend
yarn install 
yarn start
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```