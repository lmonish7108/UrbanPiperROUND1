# UrbanPiperROUND1

Development Notes: 
Set up is done on AWS Lightsails on NGINX and UWSGI.

You might see delay in Update of new stories in Server, as this is Free server and due to lack of computing power I have increased the Stories update threshold to 2 days.

To run locally you can just clone the repo.

pip install -r requirements.txt

I have added db.sqlite3 file as well, so you can directly run:

python manage.py runserver
