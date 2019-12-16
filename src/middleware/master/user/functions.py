import random
import string

from rest_framework.utils import json


# generates a random string of letters and digits
def generate_hash(length=3):
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for i in range(length))


# decodes request body
def decode_request_body(request):
    return json.loads(request.body.decode("utf-8"))
