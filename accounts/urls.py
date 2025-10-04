from django.urls import path
from .views import account
from . import views


urlpatterns = [
    path("", account, name="account"),
    path("orders/", views.orders_list, name="orders_list"),
    path(
        "orders/<str:order_number>/",
        views.order_detail,
        name="order_detail"
    ),
]
