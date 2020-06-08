# Full Stack Trivia API

## Installing Project Dependencies

Navigate to the project directory. Then create a python virtual environment. Steps to setup and activate your virtual 
environment is in the Python Docs [on this link.](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Once the python virtual environment has been activated, install the requirements by running the following command

```bash
pip install -r requirements.txt
```

## Starting the Project Server

### Frontend

Navigate to the frontend directory. Now run the following commands to start the frontend server.

```bash
npm install
npm start
```

Now the frontend is hosted on http://localhost:3000 !

### Backend

Navigate to the backend directory. Now run the following commands to start the backend server.

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Setting up the project

### Backend

1. Modify the postgres username and password in the database_path variable in models.py

### Testing

1. Modify the postgres username and password in the self.database_path variable in testing_path.py
2. Create a database with the name trivia_test
3. Run ```psql -d trivia_test -u <username> -a -f trivia.psql``` This add sample questions and categories to the test 
database. 

## API Endpoints

### 1. GET /questions

Get a list of questions paginated in groups of ten, categories, and total number of questions ignoring the pagination.
Current category that is returned is always None (null).

###### Sample requests: 

curl -X GET http://localhost:5000/questions <br>
curl -X GET http://localhost:5000/questions?page=2

###### Sample response:

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "total_questions": 19
}
```

### 2. POST /questions/search

Get a list of questions paginated in groups of ten that match the passed search query. Also get the total number of 
matches. Current category that is returned is always None (null).

Note: "searchTerm" must be passed in the body. If not, a 400 error code response will be returned.

###### Sample requests: 

curl -X POST http://localhost:5000/questions/search -d '{"searchTerm": "Lestat"}' -H "Content-Type: application/json" <br>
curl -X POST http://localhost:5000/questions/search?page=3 -d '{"searchTerm": "Steve"}' -H "Content-Type: application/json"<br>

###### Sample response:

```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "total_questions": 1
}
```

### 3. GET /categories/<category_id>/questions

Get a list of questions paginated in groups of ten that are from the category passed in the path. Also get the 
total number of questions fitting this constraint. Current category that is returned is always None (null).

###### Sample requests: 

curl -X GET http://localhost:5000/categories/2/questions
curl -X GET http://localhost:5000/categories/2/questions?page=2

###### Sample response:

```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "total_questions": 4
}
```

### 4. POST /quizzes

Get a question that's from the category passed in the body of the request. This question will also be different from the 
ones passed in the body. This ensures no question is repeated in any round.

Note: "previous_questions" and "quiz_category" must be passed in the body. If not, a 400 error code response will be returned.

###### Sample requests: 

curl -X POST http://localhost:5000/quizzes -H 'Content-Type: application/json' -d '{"previous_questions": [2, 3], "quiz_category": {"id": 2, "type": "Art"}}' <br>
curl -X POST http://localhost:5000/quizzes -H 'Content-Type: application/json' -d '{"previous_questions": [], "quiz_category": {"id": 1, "type": "Science"}}' <br>

###### Sample response:

```
{
  "question": {
    "answer": "Mona Lisa",
    "category": 2,
    "difficulty": 3,
    "id": 17,
    "question": "La Giaconda is better known as what?"
  }
}
```

### 5. GET /categories

Get a list of categories along with the number of categories

###### Sample requests: 

curl -X GET http://localhost:5000/categories

###### Sample response:

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "count_categories": 6
}
```

### 6. POST /questions

Add a question. The added question is then returned in the response.

Note: "question", "answer", "category", and "difficulty" must be passed in the body. If not, a 400 error code response will be returned.

###### Sample requests: 

curl -X POST http://localhost:5000/questions -H 'Content-Type: application/json' -d '{"question": "QUESTION", "answer": "ANSWER", "category": 2, "difficulty": 5}'

###### Sample response:

```
{
  "question": {
    "answer": "ANSWER",
    "category": 2,
    "difficulty": 5,
    "id": 26,
    "question": "QUESTION"
  }
}
```

### 6. DELETE /questions/<question_id>

Deletes a question. The deleted question is then returned in the response.

###### Sample requests: 

curl -X DELETE http://localhost:5000/questions/26

###### Sample response:

```
{
  "question": {
    "answer": "ANSWER",
    "category": 2,
    "difficulty": 5,
    "id": 26,
    "question": "QUESTION"
  }
}
```