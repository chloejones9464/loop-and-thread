from django.http import HttpResponse
import stripe


class StripeWH_Handler:
    '''Handling webhooks'''

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        '''Handling webhook events'''
        return HttpResponse(
            content=f'Unhandled webhook received : {event['type']}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        pi = event.data.object
        pi = stripe.PaymentIntent.retrieve(
            pi.id,
            expand=["payment_method", "latest_charge"]
        )

        pm_billing = pi.payment_method.billing_details
        charge_billing = pi.latest_charge.billing_details
        print("PM billing:", pm_billing)
        print("Charge billing:", charge_billing)

        return HttpResponse(
            content=f'Webhook received : {event["type"]}',
            status=200
        )

    def handle_payment_intent_failed(self, event):
        '''Handling payment_intent.failed webhook events'''
        return HttpResponse(
            content=f'Webhook received : {event['type']}',
            status=200)
