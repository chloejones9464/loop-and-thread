from django.http import HttpResponse


class StripeWH_Handler:
    '''Handling webhooks'''

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        '''Handling webhook events'''
        return HttpResponse(
            content=f'Webhook received : {event['type']}',
            status=200)