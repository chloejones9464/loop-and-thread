from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from checkout.webhook_handler import StripeWH_Handler
import logging
import traceback
import stripe


logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
def webhook(request):
    logger.info("[WH] entered /checkout/wh/")
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    wh_secret = getattr(settings, "STRIPE_WH_SECRET", "")

    # Verify signature
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
    except ValueError as e:
        logger.info("[WH] invalid payload:", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.info("[WH] bad signature:", e)
        return HttpResponse(status=400)

    event_type = event.get("type")
    logger.info("[WH] event type:", event_type)

    handler = StripeWH_Handler(request)
    event_map = {
        "payment_intent.succeeded": handler.handle_payment_intent_succeeded,
        "payment_intent.payment_failed": handler.handle_payment_intent_failed,
    }

    try:
        # Select the appropriate handler (fallback to a generic handler)
        callback = event_map.get(event_type, handler.handle_event)
        resp = callback(event)

        # If a handler forgot to return an HttpResponse, be forgiving
        if not isinstance(resp, HttpResponse):
            logger.info(
                "[WH] %s handler returned non-HttpResponse; returning 200",
                event_type,
            )
            return HttpResponse(status=200)

        return resp

    except Exception as e:
        # Log full traceback but DO NOT 500 (Stripe will retry aggressively)
        logger.info(f"[WH ERROR] {type(e).__name__}: {e}")
        logger.info(traceback.format_exc())
        return HttpResponse(status=200)