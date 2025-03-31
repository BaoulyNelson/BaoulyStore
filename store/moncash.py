import moncashify  # import the package

client_id = '187e29d7949babb0c3f4c7176b114a16'
client_secret = 'XqUTHokvglhPSmbdAeX5h_3PkHCUaQsqBem8VEcDwR5O0nDzobVKkEnNxoBmPfvw'

debug = True  # In development
moncash = moncashify.API(client_id, client_secret, debug)

# Payment
order_id = 'Tenis 023'
price = 2500  # HTG
payment = moncash.payment(order_id, price)

print('URL:', payment.redirect_url)
