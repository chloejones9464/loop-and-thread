from django.http import HttpResponse


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
        '''Handling payment_intent.succeeded webhook events'''
        return HttpResponse(
            content=f'Webhook received : {event['type']}',
            status=200)

    def handle_payment_intent_failed(self, event):
        '''Handling payment_intent.failed webhook events'''
        return HttpResponse(
            content=f'Webhook received : {event['type']}',
            status=200)