from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag!")
        return redirect(reverse('patterns'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': (
            'pk_test_51S05gHCJsBuNrC7UCIqj7QM2yYGbt'
            'Bkv2JujJoP6gfXTqztTHEEvXcuy9jpoGXPM'
            'ltgRmhay0VKK73fLx8FbRu2R00UJ3QYI4K'
        ),
        'client_secret': 'test client secret',
    }
    return render(request, template, context)
