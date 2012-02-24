cp /home/devel/deployed/current/epoch/epoch/conf/epoch.wsgi /home/devel/httpd/wsgi/
cp /home/devel/deployed/current/epoch/epoch/conf/epoch.conf /home/devel/httpd/conf.d/

service httpd restart
