from django.contrib import admin
from django.urls import path, include
from stripe_pay.views import (
    CreateCheckoutSessionView,
    ItemView,
    SuccessView,
    CancelView,
    StripeIntentView,
    OrderView,
    MainView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", MainView.as_view(), name="main"),
    path("item/<pk>/", ItemView.as_view(), name="item"),
    path(
        "buy/<int:pk>/",
        CreateCheckoutSessionView.as_view(),
        name="buy",
    ),
    path(
        "order-buy/<pk>/",
        StripeIntentView.as_view(),
        name="order-buy",
    ),
    path(
        "order/<pk>/",
        OrderView.as_view(),
        name="order",
    ),
]
