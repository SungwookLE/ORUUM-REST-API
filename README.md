# ORUUM-REST-API
> Author: ORUUM  

## Environment
- ubuntu 20.04LTS
- python=3.10
- django=4.0
- djangorestframework=3.13.1
- misc. packages: [requirements](./requirements.txt)

## Project
- Tree
```
.
├── accounts
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── __pycache__
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── api
│   ├── admin.py
│   ├── apps.py
│   ├── converters.py
│   ├── __init__.py
│   ├── models.py
│   ├── __pycache__
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── backend
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings
│   │   ├── base.py
│   │   ├── develop.py
│   │   ├── __init__.py
│   │   ├── product.py
│   │   └── __pycache__
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── dashboard
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── plotly_set.py
│   ├── __pycache__
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db_handler
│   ├── dbModule.py
│   ├── get_stocks_oruum.py
│   ├── __pycache__
│   └── update_stocks_yahooapi.py
├── manage.py
├── README.md
├── requirements.txt
├── static
└── templates
    ├── home.html
    ├── test1_dashplot.html
    └── test2_dashplot.html
```
