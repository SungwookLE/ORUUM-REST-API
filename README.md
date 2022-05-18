# ORUUM-REST-API
> Author: ORUUM  

## Environment
- ubuntu 20.04LTS
- python=3.10
- django=4.0
- djangorestframework=3.13.1
- Misc Packages: [requirements](./requirements.txt)

## Project
- Tree
```
├── accounts
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── api
│   ├── admin.py
│   ├── apps.py
│   ├── converters.py
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── backend
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings
│   │   ├── base.py
│   │   ├── develop.py
│   │   ├── __init__.py
│   │   └── product.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── dashboard
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── plotly_plot.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db_parser
│   ├── dbModule.py
│   ├── parser_stock_list.py
│   └── recive_from_oruum.py
├── manage.py
├── README.md
├── static
└── templates
    ├── home.html
    ├── test1_dashplot.html
    └── test2_dashplot.html
```
