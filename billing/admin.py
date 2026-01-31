from django.contrib import admin
from .models import Product, Invoice, InvoiceItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Ce qu'on affiche dans la liste des produits (admin)
    list_display = ("id", "name", "price", "expiration_date")


class InvoiceItemInline(admin.TabularInline):
    # Permet de voir/éditer les lignes directement dans une facture (admin)
    model = InvoiceItem
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    inlines = [InvoiceItemInline]


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ("id", "invoice", "product", "quantity", "unit_price")
