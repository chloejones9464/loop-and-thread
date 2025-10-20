from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    print("[WH] entered /checkout/wh/")
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    wh_secret = settings.STRIPE_WH_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
    except ValueError as e:
        print("[WH] invalid payload:", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print("[WH] bad signature:", e)
        return HttpResponse(status=400)

    print("[WH] event type:", event.get("type"))
    handler = StripeWH_Handler(request)
    event_map = {
        "payment_intent.succeeded": handler.handle_payment_intent_succeeded,
        "payment_intent.payment_failed": handler.handle_payment_intent_failed,
    }
    return event_map.get(event.get("type"), handler.handle_event)(event)
