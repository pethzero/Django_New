@echo off
call .\envdjango\Scripts\activate
python manage.py runserver
call .\envdjango\Scripts\deactivate