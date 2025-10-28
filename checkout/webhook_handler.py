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
            print("[WH] ABORT no recipient")
            return 0

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

        metadata = intent.get('metadata') or {}
        bag_json = metadata.get('bag') or '{}'
        try:
            if isinstance(bag_json, str):
                bag = json.loads(bag_json)
            else:
                bag = bag_json or {}
        except Exception:
            print("[WH] Could not parse bag JSON; defaulting to empty.")
            bag = {}

        if not bag:
            print("[WH] No bag in metadata; skipping order creation.")
            return HttpResponse(status=200)

        charge = None
        try:
            charges = intent.get("charges", {}).get("data", [])
            if charges:
                charge = charges[0]
        except Exception:
            charge = None

        billing = (charge or {}).get("billing_details", {}) or {}
        shipping = intent.get("shipping", {}) or {}
        address_b = billing.get("address", {}) or {}
        address_s = shipping.get("address", {}) or {}

        name = (
            billing.get("name")
            or shipping.get("name")
            or ""
        ).strip()
        email = (billing.get("email") or "").strip()
        phone = (
            billing.get("phone")
            or shipping.get("phone")
            or ""
        ).strip()

        country_b = address_b.get("country") or ""
        country_s = address_s.get("country") or ""
        country = (country_b or country_s).strip()

        postcode_b = address_b.get("postal_code") or ""
        postcode_s = address_s.get("postal_code") or ""
        postcode = (postcode_b or postcode_s).strip()

        city_b = address_b.get("city") or ""
        city_s = address_s.get("city") or ""
        city = (city_b or city_s).strip()

        line1_b = address_b.get("line1") or ""
        line1_s = address_s.get("line1") or ""
        line1 = (line1_b or line1_s).strip()

        line2_b = address_b.get("line2") or ""
        line2_s = address_s.get("line2") or ""
        line2 = (line2_b or line2_s).strip()

        state_b = address_b.get("state") or ""
        state_s = address_s.get("state") or ""
        state = (state_b or state_s).strip()

        amount_cents = (charge or {}).get("amount")
        if amount_cents is None:
            amount_cents = intent.get("amount", 0) or 0
        order_total_amount = (
            Decimal(str(amount_cents)) / Decimal("100")
        ).quantize(Decimal("0.01"))

        if not name:
            print(
                "[WH] Missing name (billing + shipping empty)."
                " Skipping order creation."
            )
            return HttpResponse(status=200)

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=name or "",
                    email__iexact=email or "",
                    phone_number__iexact=phone or "",
                    country__iexact=country or "",
                    postcode__iexact=postcode or "",
                    town_or_city__iexact=city or "",
                    street_address1__iexact=line1 or "",
                    street_address2__iexact=line2 or "",
                    county__iexact=state or "",
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
            message = (
                f"Webhook received : {event['type']} "
                f"| Order already in database"
            )
            return HttpResponse(
                content=message,
                status=200
            )

        try:
            order = Order.objects.create(
                full_name=name,
                email=email or "",
                phone_number=phone,
                country=country,
                postcode=postcode,
                town_or_city=city,
                street_address1=line1,
                street_address2=line2,
                county=state,
                original_bag=bag_json,
                stripe_pid=pid,
            )

            items_iter = bag.items() if hasattr(bag, "items") else []
            for item_id_str, item_data in items_iter:
                try:
                    pattern = Pattern.objects.get(pk=int(item_id_str))
                except Pattern.DoesNotExist:
                    print(
                        f"[WH] Pattern {item_id_str} not found;"
                        " skipping line item."
                    )
                    continue
                OrderLineItem.objects.create(order=order, pattern=pattern)

        except Exception as e:
            if 'order' in locals():
                try:
                    order.delete()
                except Exception:
                    pass
            return HttpResponse(
                content=f"Webhook received : {event['type']} | ERROR: {e}",
                status=200
            )

        self._send_confirmation_email(order)
        return HttpResponse(
            content=f"Webhook received : {event['type']}"
            " | SUCCESS: Created order in webhook",
            status=200
        )

    def handle_payment_intent_failed(self, event):
        return HttpResponse(
            content=f"Webhook received : {event['type']}",
            status=200
        )
