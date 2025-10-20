from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.mail import get_connection
from django.template.loader import render_to_string
from django.conf import settings
from decimal import Decimal
from .models import Order, OrderLineItem
from patterns.models import Pattern
import time
import json
import stripe


class StripeWH_Handler:
    def __init__(self, request):
        self.request = request
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

        cust_email = (order.email or
                    getattr(getattr(
                        order,
                        "user_profile",
                        None), "user", None).email or "").strip()
        print(f"[WH] preparing email to: {cust_email or '<EMPTY>'}")
        if not cust_email:
            print("[WH] ABORT no recipient"); return 0

        connection = get_connection(
            "django.core.mail.backends.console.EmailBackend"
            )

        subject = render_to_string(
            "checkout/confirmation_emails/confirmation_email_subject.txt",
                                {"order": order}).strip().replace("\n", " ")
        body = render_to_string(
            "checkout/confirmation_emails/confirmation_email_body.txt",
            {"order": order, "contact_email": settings.DEFAULT_FROM_EMAIL})
        sent = send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email],
            connection=connection)
        print("[WH] send_mail returned:", sent)
        return sent

    def handle_event(self, event):
        return HttpResponse(
            content=f"Unhandled webhook received : {event['type']}",
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        print("[WH] payment_intent.succeeded received")
        intent = event['data']['object']
        pid = intent['id']

        bag_json = intent.get('metadata', {}).get('bag', '{}')
        bag = json.loads(bag_json)
        save_info = intent.get('metadata', {}).get('save_info')

        stripe_charge = stripe.Charge.retrieve(intent['latest_charge'])
        billing = stripe_charge['billing_details']
        amount_decimal = Decimal(stripe_charge['amount']) / Decimal('100')
        order_total_amount = amount_decimal.quantize(Decimal('0.01'))

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=billing.get('name', ''),
                    email__iexact=billing.get('email', ''),
                    phone_number__iexact=(
                        billing.get('phone', '')
                    ),
                    country__iexact=(
                        billing.get('address', {}).get('country', '')
                    ),
                    postcode__iexact=(
                        billing.get('address', {})
                        .get('postal_code', '')
                    ),
                    town_or_city__iexact=(
                        billing.get('address', {})
                        .get('city', '')
                    ),
                    street_address1__iexact=billing.get('address', {}).get(
                        'line1', ''
                    ),
                    street_address2__iexact=billing.get('address', {}).get(
                        'line2', ''
                    ),
                    county__iexact=billing.get('address', {}).get(
                        'state', ''
                    ),
                    order_total=order_total_amount,
                    original_bag=bag_json,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=(
                    f"Webhook received : {event['type']} | "
                    "Order already in database"
                ),
                status=200
            )

        try:
            order = Order.objects.create(
                full_name=billing.get('name', ''),
                email=billing.get('email', ''),
                phone_number=billing.get('phone', ''),
                country=billing.get('address', {}).get('country', ''),
                postcode=billing.get('address', {}).get('postal_code', ''),
                town_or_city=billing.get('address', {}).get('city', ''),
                street_address1=billing.get('address', {}).get('line1', ''),
                street_address2=billing.get('address', {}).get('line2', ''),
                county=billing.get('address', {}).get('state', ''),
                original_bag=bag_json,
                stripe_pid=pid,
            )

            for item_id_str, item_data in bag.items():
                pattern = Pattern.objects.get(pk=int(item_id_str))
                OrderLineItem.objects.create(order=order, pattern=pattern)

        except Exception as e:
            if 'order' in locals():
                order.delete()
            return HttpResponse(
                content=f"Webhook received : {event['type']} | ERROR: {e}",
                status=500
            )
        self._send_confirmation_email(order)
        return HttpResponse(
            content=(
                f"Webhook received : {event['type']} | "
                "SUCCESS: Created order in webhook"
            ),
            status=200
        )

    def handle_payment_intent_failed(self, event):
        return HttpResponse(
            content=f"Webhook received : {event['type']}",
            status=200
        )
