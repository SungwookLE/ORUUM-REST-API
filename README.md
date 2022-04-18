# ORUUM-REST-API
> Authority: ORUUM  

## Package(@ubuntu 20.04LTS)
- python=3.10
- django=4.0
- djangorestframework=3.13.1
- See the [requirements](./requirements.txt)

## Tree

├── 220413_rdb_erd.mwb
├── accounts
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-310.pyc
│   │       └── __init__.cpython-310.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── admin.cpython-310.pyc
│   │   ├── apps.cpython-310.pyc
│   │   ├── __init__.cpython-310.pyc
│   │   └── models.cpython-310.pyc
│   ├── tests.py
│   └── views.py
├── api
│   ├── admin.py
│   ├── apps.py
│   ├── converters.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_stock_list_ticker_and_more.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-310.pyc
│   │       ├── 0002_alter_stockinformation_id.cpython-310.pyc
│   │       ├── 0002_alter_stock_list_ticker_and_more.cpython-310.pyc
│   │       ├── 0003_alter_stockinformation_id_and_more.cpython-310.pyc
│   │       ├── 0004_alter_stockinformation_id.cpython-310.pyc
│   │       ├── 0005_alter_stockinformation_symbol.cpython-310.pyc
│   │       ├── 0006_remove_stockinformation_id_and_more.cpython-310.pyc
│   │       ├── 0007_alter_stockinformation_symbol.cpython-310.pyc
│   │       ├── 0008_stockhistory.cpython-310.pyc
│   │       ├── 0009_stockinformation_date_stockprice_date_and_more.cpython-310.pyc
│   │       ├── 0010_alter_stockhistory_dividends_and_more.cpython-310.pyc
│   │       ├── 0011_stockhistory_aapl_stockhistory_msft_and_more.cpython-310.pyc
│   │       ├── 0012_stockhistory_remove_stockhistory_msft_symbol_and_more.cpython-310.pyc
│   │       ├── 0013_alter_stockhistory_date.cpython-310.pyc
│   │       ├── 0014_alter_stockhistory_adj_close_and_more.cpython-310.pyc
│   │       ├── 0015_stock_information_history_stock_list_and_more.cpython-310.pyc
│   │       ├── 0016_alter_stock_list_ticker_and_more.cpython-310.pyc
│   │       ├── 0017_remove_stock_list_id_alter_stock_list_ticker.cpython-310.pyc
│   │       └── __init__.cpython-310.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── admin.cpython-310.pyc
│   │   ├── apps.cpython-310.pyc
│   │   ├── converters.cpython-310.pyc
│   │   ├── __init__.cpython-310.pyc
│   │   ├── models.cpython-310.pyc
│   │   ├── serializers.cpython-310.pyc
│   │   ├── urls.cpython-310.pyc
│   │   └── views.cpython-310.pyc
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── backend
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── settings.cpython-310.pyc
│   │   ├── urls.cpython-310.pyc
│   │   ├── views.cpython-310.pyc
│   │   └── wsgi.cpython-310.pyc
│   ├── settings
│   │   ├── base.py
│   │   ├── develop.py
│   │   ├── __init__.py
│   │   ├── product.py
│   │   └── __pycache__
│   │       ├── base.cpython-310.pyc
│   │       ├── develop.cpython-310.pyc
│   │       └── __init__.cpython-310.pyc
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── manage.py
├── README.md
├── requirements.txt
├── static
└── templates
    └── home.html
 
## Reference
- [Django official Docs](https://docs.djangoproject.com/ko/4.0/)
- [Django-REST-Framework](https://www.django-rest-framework.org/)
- [Classy Django REST Framework](https://www.cdrf.co/)
