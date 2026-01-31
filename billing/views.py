from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product, Invoice


# -----------------------------
# PRODUITS (CRUD + pagination)
# -----------------------------

def product_list(request: HttpRequest) -> HttpResponse:
    # Récupère tous les produits (du plus récent au plus ancien)
    qs = Product.objects.order_by("-id")

    # Pagination : 10 produits par page
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "billing/products/list.html", {"page_obj": page_obj})


def product_create(request: HttpRequest) -> HttpResponse:
    # Affiche un formulaire vide (GET) ou traite la création (POST)
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/products/")
    else:
        form = ProductForm()

    return render(request, "billing/products/form.html", {"form": form, "mode": "create"})


def product_update(request: HttpRequest, pk: int) -> HttpResponse:
    # Récupère le produit à modifier
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("/products/")
    else:
        form = ProductForm(instance=product)

    return render(request, "billing/products/form.html", {"form": form, "mode": "update", "product": product})


def product_delete(request: HttpRequest, pk: int) -> HttpResponse:
    # Page de confirmation + suppression (POST)
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect("/products/")

    return render(request, "billing/products/confirm_delete.html", {"product": product})


# -----------------------------
# FACTURES (stubs pour l'instant)
# -----------------------------

def invoice_list(request: HttpRequest) -> HttpResponse:
    # Placeholder : on implémente après
    return render(request, "billing/invoices/list.html", {})


def invoice_create(request: HttpRequest) -> HttpResponse:
    # Placeholder : on implémente après
    return render(request, "billing/invoices/form.html", {})


def invoice_detail(request: HttpRequest, pk: int) -> HttpResponse:
    # Placeholder : on implémente après
    return render(request, "billing/invoices/detail.html", {})
