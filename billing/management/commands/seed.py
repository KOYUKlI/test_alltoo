import random
from decimal import Decimal
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from billing.models import Product, Invoice, InvoiceItem


class Command(BaseCommand):
    help = "Génère des données de test (produits + factures + lignes)."

    def add_arguments(self, parser):
        parser.add_argument("--products", type=int, default=25, help="Nombre de produits à créer")
        parser.add_argument("--invoices", type=int, default=15, help="Nombre de factures à créer")
        parser.add_argument("--max-lines", type=int, default=6, help="Nb max de lignes par facture")
        parser.add_argument("--clear", action="store_true", help="Supprime les données avant de seed")

    @transaction.atomic
    def handle(self, *args, **options):
        products_n = options["products"]
        invoices_n = options["invoices"]
        max_lines = options["max_lines"]
        do_clear = options["clear"]

        if do_clear:
            # Ordre important: items -> invoices -> products
            InvoiceItem.objects.all().delete()
            Invoice.objects.all().delete()
            Product.objects.all().delete()
            self.stdout.write(self.style.WARNING("Données supprimées (clear)."))

        # 1) Produits
        created_products = []
        base_names = [
            "Pâtes", "Riz", "Lait", "Beurre", "Fromage", "Jus", "Eau", "Soda", "Café", "Thé",
            "Pain", "Chocolat", "Biscuits", "Yaourt", "Farine", "Sucre", "Sel", "Poivre", "Huile", "Vinaigre",
        ]

        for i in range(products_n):
            name = f"{random.choice(base_names)} {i+1}"
            price = Decimal(random.randrange(50, 2500)) / Decimal("100")  # 0.50€ à 25.00€
            # Date de péremption: parfois proche, parfois plus loin, parfois None
            if random.random() < 0.15:
                expiration = None
            else:
                expiration = date.today() + timedelta(days=random.randint(5, 365))

            p = Product.objects.create(
                name=name,
                price=price,
                expiration_date=expiration,
            )
            created_products.append(p)

        self.stdout.write(self.style.SUCCESS(f"{len(created_products)} produits créés."))

        if not created_products:
            self.stdout.write(self.style.ERROR("Aucun produit, seed factures impossible."))
            return

        # 2) Factures + lignes
        for _ in range(invoices_n):
            invoice = Invoice.objects.create()

            # nombre de lignes (1..max_lines)
            lines_count = random.randint(1, max_lines)

            # choisir des produits distincts pour éviter conflit unique_together
            chosen = random.sample(created_products, k=min(lines_count, len(created_products)))

            for product in chosen:
                qty = random.randint(1, 8)

                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=qty,
                    unit_price=product.price,  # snapshot
                )

        self.stdout.write(self.style.SUCCESS(f"{invoices_n} factures créées."))
        self.stdout.write(self.style.SUCCESS("Seed terminé."))
