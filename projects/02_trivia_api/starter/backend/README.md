# Backend - Full Stack Trivia API Reference

## Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys.

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "error": 404,
    "message": "not found"
}
```
The API will return three error types when requests fail:
- 404: Resource Not Found
- 422: Not Processable

## Endpoints

### GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Argument: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key: value pairs
```
{   
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
}
```
### GET '/api/v1.0/questions'
- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Argument: page = integer
- Returns: A json object contains 10 paginated questions, number of total questions, dictionary object including all categories and current category string.
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}
```
### DELETE '/api/v1.0/questions/<int:id>
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: The appropriate HTTP status code

### POST '/api/v1.0/questions'
- Sends a post request in order to add a new question
- Request body:
```
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
```
- Returns: The appropriate HTTP status code

### POST '/api/v1.0/questions'
- Sends a post request in order to search for a specific question by search term.
- Request body:
```
{
        'searchTerm': 'this is the term the user is looking for'
}
```
- Returns: any array of questions, a number of total questions and the current category string
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}
```
### GET '/api/v1.0/categories/<int:id>/questions'
- Fetches questions for a category specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, number of total questions and current category string
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```
### POST '/api/v1.0/quizzes'
- Sends a post requested in order to get the next question
- Request body:
{'previous_questions':  an array of question id's such as [1, 4, 20, 15]
'quiz_category': a string of the current category }
- Returns: a single a new question object
```
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer', 
        'difficulty': 5,
        'category': 4
    }
}
```