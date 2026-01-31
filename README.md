# Test Alltoo — Générateur de factures (Django)

## Prérequis
- Python 3.13+
- Windows (CMD / VS Code terminal)

## Installation
```bat
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
````

## Base de données

```bat
py manage.py makemigrations
py manage.py migrate
```

## Données de test (seed)
Génère des produits + factures pour tester la pagination et les totaux.

```bat
py manage.py seed --clear --products 25 --invoices 15 --max-lines 6

## Lancer l'app

```bat
py manage.py runserver
```

Ouvrir : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## URLs

* Produits (CRUD + pagination) :

  * Liste : [http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/)
  * Créer : [http://127.0.0.1:8000/products/new/](http://127.0.0.1:8000/products/new/)

* Factures (création + lignes dynamiques + quantité) :

  * Liste : [http://127.0.0.1:8000/invoices/](http://127.0.0.1:8000/invoices/)
  * Créer : [http://127.0.0.1:8000/invoices/new/](http://127.0.0.1:8000/invoices/new/)

## Notes fonctionnelles

* Le prix d’un produit ne peut pas être négatif (validation + contrainte DB).
* Une facture doit contenir au moins 1 ligne (validation serveur + UX).
* Les doublons de produits dans une facture sont fusionnés (quantités additionnées).
* Le prix unitaire est snapshotté au moment de la création de la facture.