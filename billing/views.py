from decimal import Decimal

from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import InvoiceLineFormSet, ProductForm
from .models import Invoice, InvoiceItem, Product


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
# FACTURES (list/create/detail)
# -----------------------------

def invoice_list(request: HttpRequest) -> HttpResponse:
    # Liste des factures (du plus récent au plus ancien)
    qs = Invoice.objects.order_by("-id")

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "billing/invoices/list.html", {"page_obj": page_obj})


def invoice_create(request: HttpRequest) -> HttpResponse:
    """
    Crée une facture à partir d'un formset de lignes (produit + quantité).
    Important : on ne crée la facture en base QUE si le formset est valide.
    """
    if request.method == "POST":
        formset = InvoiceLineFormSet(request.POST, prefix="items")
        if formset.is_valid():
            # Crée la facture maintenant (car on sait qu'on a au moins 1 ligne valide)
            invoice = Invoice.objects.create()

            # Merge des produits identiques (si l'utilisateur a mis le même produit 2 fois)
            merged = {}  # product_id -> {"product": Product, "qty": int}

            for form in formset:
                if not hasattr(form, "cleaned_data"):
                    continue
                if form.cleaned_data.get("DELETE"):
                    continue

                product = form.cleaned_data.get("product")
                qty = form.cleaned_data.get("quantity")

                if not product or not qty:
                    continue

                if product.id in merged:
                    merged[product.id]["qty"] += qty
                else:
                    merged[product.id] = {"product": product, "qty": qty}

            # Crée les lignes de facture en snapshotant le prix
            for data in merged.values():
                product = data["product"]
                qty = data["qty"]

                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=qty,
                    unit_price=product.price,  # snapshot du prix
                )

            return redirect(f"/invoices/{invoice.id}/")
    else:
        formset = InvoiceLineFormSet(prefix="items")

    return render(request, "billing/invoices/form.html", {"formset": formset})


def invoice_detail(request: HttpRequest, pk: int) -> HttpResponse:
    invoice = get_object_or_404(Invoice, pk=pk)

    items = invoice.items.select_related("product").order_by("id")
    total_qty = sum(i.quantity for i in items)
    total_amount = sum((i.line_total for i in items), Decimal("0.00"))

    return render(
        request,
        "billing/invoices/detail.html",
        {
            "invoice": invoice,
            "items": items,
            "total_qty": total_qty,
            "total_amount": total_amount,
        },
    )
