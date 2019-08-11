## Remote url downloader

> #### This project basically exposes an endpoint for downloading given list of urls. After downloading them it makes a zip file and sends this zip to given email id

----

### Usage
> Make a virtual environment and activate it

> `pip install -r requirements.txt`

> Then go to settings.py and edit `EMAIL_HOST_USERNAME` and `EMAIL_HOST_PASSWORD`. Basically these are used for sending emails

> `python manage.py runserver 8000`

> Open a new terminal and run celery worker here
`celery -A adnabu worker -l info`

> Now you make a post call with list of urls and email at `http://localhost:8000/downloads/`  

