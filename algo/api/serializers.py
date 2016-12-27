from flask_restplus import fields
from algo.api.restplus import api


status = api.model('App status', {
    'status': fields.String(required=True, description='App status'),
})

payload = api.model('request payload', {
})
