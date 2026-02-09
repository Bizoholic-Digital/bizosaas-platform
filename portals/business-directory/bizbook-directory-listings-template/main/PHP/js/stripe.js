Stripe.setPublishableKey('pk_test_oeP6xrVYPkQhUkfbkyApYzsI006jhjc2ty');  // set your stripe publishable key
$(document).ready(function() {
    $("#payment_stripe_form").submit(function(event) {
        $('#stripe_payment_submit').attr("disabled", "disabled");
// create stripe token to make payment
        Stripe.createToken({
            number: $('#card_number').val(),
            cvc: $('#cardCVC').val(),
            exp_month: $('#cardExpMonth').val(),
            exp_year: $('#cardExpYear').val()
        }, handleStripeResponse);
        return false;
    });
});
// handle the response from stripe
function handleStripeResponse(status, response) {
    console.log(JSON.stringify(response));
    if (response.error) {
        $('#stripe_payment_submit').removeAttr("disabled");
        $(".paymentErrors").html(response.error.message);
    } else {
        var payForm = $("#payment_stripe_form");
//get stripe token id from response
        var stripeToken = response['id'];
//set the token into the form hidden input to make payment
        payForm.append("<input type='hidden' name='stripeToken' value='" + stripeToken + "' />");
        payForm.get(0).submit();
    }
}