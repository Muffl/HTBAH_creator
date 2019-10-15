#export LC_ALL=C.UTF-8
#export FLASK_APP=webfrontend.py
#
#flask run -h 0.0.0.0 -p 4950
#
#if DEBUG == 'NO':
#	source venvcode/bin/activate
gunicorn-3.6 -b 0.0.0.0:5000 --access-logfile - --error-logfile - webfrontend:app
