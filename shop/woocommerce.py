from woocommerce import API
from django.conf import settings

api = API(
    url=settings.WOO_API_URL,
    consumer_key=settings.WOO_CONSUMER_KEY,
    consumer_secret=settings.WOO_CONSUMER_SECRET,
    version="wc/v3"
)

def get_all_customers():
    return api.get('customers').json()

def update_customer(customer_id, data):
    uri = 'customers/{}'.format(customer_id)
    return api.put(uri, data).json()

def create_customer(data):
    return api.post('customers', data).json()

def delete_customer(customer_id):
    uri = 'customers/{}?force=true'.format(customer_id)
    return api.delete(uri).json()

def get_customer(customer_id):
    uri = 'customers/{}'.format(customer_id)
    return api.get(uri).json()