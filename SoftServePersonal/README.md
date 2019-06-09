instalation
download from github, make venv install reqirements.txt

1. make migrations
2. run server
3. run selery beat
``celery -A SoftServePersonal beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler``
4. run worker
``celery -A SoftServePersonal worker -E --loglevel=info``