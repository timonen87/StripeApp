from django.contrib import admin
from django.urls import path, include
from stripe_pay.views import (
    CreateCheckoutSessionView,
    ItemView,
    SuccessView,
    CancelView,
    stripe_webhook,
    StripeIntentView,
    OrderView,
    IndexView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
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
    path("webhooks/stripe/", stripe_webhook, name="stripe-webhook"),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("success/", SuccessView.as_view(), name="success"),
    path(
        "order/<pk>/",
        OrderView.as_view(),
        name="order",
    ),
]
