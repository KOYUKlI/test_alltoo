from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # racine -> produits
    path("", lambda request: redirect("/products/")),

    # routes de l'app billing
    path("", include("billing.urls")),
]
