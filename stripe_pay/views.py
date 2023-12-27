import json
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import DetailView
from .models import Item, Order


stripe.api_key = settings.STRIPE_SECRET_KEY


class IndexView(TemplateView):
    template_name = "base.html"


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class ItemView(TemplateView):
    template_name = "item.html"

    def get_context_data(self, **kwargs):
        item_id = self.kwargs["pk"]
        item = Item.objects.get(id=item_id)
        context = super(ItemView, self).get_context_data(**kwargs)
        context.update({"item": item, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY})
        return context


class OrderView(TemplateView):
    template_name = "order.html"

    def get_context_data(self, **kwargs):
        order_id = self.kwargs["pk"]
        order = Order.objects.get(id=order_id)
        context = super(OrderView, self).get_context_data(**kwargs)
        context.update(
            {"order": order, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY}
        )
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs["pk"]
        item = Item.objects.get(id=item_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": item.currency,
                        "unit_amount": item.price,
                        "product_data": {"name": item.name},
                    },
                    "quantity": 1,
                },
            ],
            metadata={"item_id": item.id},
            mode="payment",
            success_url=YOUR_DOMAIN + "/success/",
            cancel_url=YOUR_DOMAIN + "/cancel/",
        )
        return JsonResponse({"id": checkout_session.id})


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json["email"])
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            intent = stripe.PaymentIntent.create(
                amount=order.total_price,
                currency=order.currency,
                customer=customer["id"],
                metadata={"order_id": order.id},
            )
            return JsonResponse({"clientSecret": intent["client_secret"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        customer_email = session["customer_details"]["email"]
        item_id = session["metadata"]["product_id"]

        item = Item.objects.get(id=item_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {item.url}",
            recipient_list=[customer_email],
            from_email="matt@test.com",
        )

        # TODO - decide whether you want to send the file or the URL

    elif event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer["email"]
        item_id = intent["metadata"]["item_id"]

        item = Item.objects.get(id=item_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {item.url}",
            recipient_list=[customer_email],
            from_email="matt@test.com",
        )

    return HttpResponse(status=200)
