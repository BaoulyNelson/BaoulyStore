// === PayPal ===
paypal.Buttons({
    createOrder: function(data, actions) {
        return actions.order.create({
            purchase_units: [{
                amount: { value: '10.00' }
            }]
        });
    },
    onApprove: function(data, actions) {
        return actions.order.capture().then(function(details) {
            alert('Paiement réussi par ' + details.payer.name.given_name);
        });
    }
}).render('#paypal-button-container');

// === Stripe ===
var stripe = Stripe('VOTRE_CLE_PUBLIQUE_STRIPE');
document.getElementById('stripe-button').addEventListener('click', function () {
    fetch('/create-checkout-session', { method: 'POST' })
        .then(response => response.json())
        .then(session => stripe.redirectToCheckout({ sessionId: session.id }))
        .catch(error => console.error('Erreur Stripe:', error));
});