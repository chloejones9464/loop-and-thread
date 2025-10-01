var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var card = elements.create('card', { style: style });

var style = {
    base: {
        color: '#393949ff',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSize: '16px',
        '::placeholder': { color: '#aab7c4' }
    },
    invalid: { color: '#fa755a' }
};

var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var card = elements.create('card', { style: style });
card.mount('#card-element');

card.on('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
        <span class="icon" role="alert"><i class="fas fa-times"></i></span>
        <span>${event.error.message}</span>`;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

function showLoader() {
    const $ov = $('.loading-spinner');
    $ov.css('display', 'flex').hide().fadeIn(120);
    $('body').css('overflow', 'hidden');
}
function hideLoader() {
    $('.loading-spinner').fadeOut(120, function () {
        $(this).hide();
        $('body').css('overflow', '');
    });
}


var form = document.getElementById('checkout-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({ disabled: true });
    $('#submit-button').attr('disabled', true);

    showLoader();

    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    var url = '/checkout/cache_checkout_data/';
    $.post(url, postData).done(function () {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address: {
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value),
                    }
                }
            }
        }).then(function (result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
        <span class="icon" role="alert"><i class="fas fa-times"></i></span>
        <span>${result.error.message}</span>`;
                $(errorDiv).html(html);

                hideLoader();
                card.update({ disabled: false });
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        location.reload();
    });
});