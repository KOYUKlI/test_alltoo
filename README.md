````md
# Test Alltoo — Générateur de factures (Django)

## Setup
```bash
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
````

## Run

```bash
py manage.py migrate
py manage.py runserver
```

## URLs

* Produits: [http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/)
* Factures: [http://127.0.0.1:8000/invoices/](http://127.0.0.1:8000/invoices/)

````
