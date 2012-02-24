Epoch! : PBS management tool for Righscale environments
=========================================

Install for dev::

   git clone git@github.com:pbs/epoch.git

reconfigure epoch/settings.py if you want

create a virtual environment:: 
   virtualenv --distribute ve --prompt='(epoch)'
activate virtual environment::
   . ./ve/bin/activate
install the project::
   python setup.py develop
create database and models::
   django-admin.py syncdb --settings=epoch.settings
run the server for local development::
   django-admin.py runserver 127.0.0.1 --settings=epoch.settings