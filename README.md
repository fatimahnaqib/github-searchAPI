# Application Setup

The instruction given below will enable the application to run locally for testing purposes.

1. Create a virtual environment: 

```
virtualenv env
```

2. Start virtual environment (Windows):

```
env\Scripts\activate
```

3. Install packages from requirement.txt:

```
pip install -r requirements.txt
```

4. Setup up model:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

5. Run server:

```
python manage.py runserver
```

Server runs at: 127.0.0.1:8000/

6. To execute the tests , please run the following from the directory containing the tests.py file:

```
pytest tests.py
```