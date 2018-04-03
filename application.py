from app import flaskApp as application
application.debug = True
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.run()


# export FLASK_APP=application.py
# export LANG=en_US.utf-8
# export LC_ALL=en_US.utf-8
# flask run
# pip install -r requirements.txt.


# eb init -p python-3.4 web-dev
# eb init
# eb create web-dev
# eb deploy     (needs a new git commit for it to work)
# eb open