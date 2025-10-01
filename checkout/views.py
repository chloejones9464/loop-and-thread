from django.shortcuts import (
    render,
    redirect,
    reverse,
    get_object_or_404,
    HttpResponse,
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
import stripe
import json

from .forms import OrderForm
from patterns.models import Pattern
from .models import Order, OrderLineItem
from bag.contexts import bag_contents


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})

    if request.method == 'POST':
        if not bag:
            messages.error(request, "There's nothing in your bag!")
            return redirect(reverse('patterns'))

        form_data = {
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''),
            'phone_number': request.POST.get('phone_number', ''),
            'country': request.POST.get('country', ''),
            'postcode': request.POST.get('postcode', ''),
            'town_or_city': request.POST.get('town_or_city', ''),
            'street_address1': request.POST.get('street_address1', ''),
            'street_address2': request.POST.get('street_address2', ''),
            'county': request.POST.get('county', ''),
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id in bag.keys():
                try:
                    pattern = Pattern.objects.get(pk=item_id)
                except Pattern.DoesNotExist:
                    messages.error(
                        request,
                        (
                            "One of the patterns in your bag "
                            "wasn't found."
                        )
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

                OrderLineItem.objects.create(
                    order=order,
                    pattern=pattern,
                    lineitem_total=pattern.price,
                )
            request.session['save_info'] = 'save-info' in request.POST
            request.session['bag'] = {}
            return redirect(reverse(
                'checkout_success',
                args=[order.order_number]
                ))
        else:
            messages.error(
                request,
                (
                    "There was an error with your form. "
                    "Please double-check your information."
                )
            )
            return redirect(reverse('checkout'))

    if not bag:
        messages.error(request, "There's nothing in your bag!")
        return redirect(reverse('patterns'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = int(round(total * 100))

    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
        automatic_payment_methods={'enabled': True},
    )

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(
            request,
            ("Stripe public key is missing — did you set it in env.py?")
        )

    return render(request, 'checkout/checkout.html', {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    })


def checkout_success(request, order_number):
    '''
    Handles the successful checkout
    '''
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, "Order has been processed successfully!")

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    
    return render(request, template, context)