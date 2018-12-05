uwsgi --buffer-size 65535 --socket 0.0.0.0:5000 --protocol=http  --master -w wsgi:app
