uwsgi --cache2  name=mapcache,items=100 --buffer-size 65535 --socket 0.0.0.0:5000 --protocol=http  --master -w wsgi:app --enable-threads --lazy-apps --catch-exceptions --py-autoreload=3 
