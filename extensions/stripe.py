import os
import stripe


stripe_keys = {
    'secret_key': os.environ.get('STRIPE_SECRET_KEY', 'sk_test_51OIQ9qKbFgjv6nDDqAa2yUY42xtcofWmf05Xw9eEL98E4jfAOdRRFKXxlVZtJwDEDxnSN5SMHHjAmYr2QuJMjkwm00GXVsAG5B'),
    'publishable_key': os.environ.get('STRIPE_PUBLISHABLE_KEY', 'pk_test_51OIQ9qKbFgjv6nDD90oaCUnoZtnJtido7wvm5Wje9xwfxHtsFoPVaZul8uKHK0Y6V3RpQamWI3cD6o66X7neIqH400TRqsnHHK')
}

stripe.api_key = stripe_keys['secret_key']
