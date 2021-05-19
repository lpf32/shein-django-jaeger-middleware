import requests
from opentracing.ext import tags
from opentracing import Format

from . import tracer


def jaeger_decorator(method):
    def inner(fn):
        def __decorator(*args, **kwargs):
            url = args[0]
            span_tags = {tags.HTTP_METHOD: 'GET', tags.HTTP_URL: url, tags.SPAN_KIND: tags.SPAN_KIND_RPC_CLIENT}
            if 'headers' in kwargs:
                headers = kwargs.get('headers')
            else:
                headers = {}
            operation_name = 'outbound-{}'.format(url)
            with tracer.start_span(operation_name=operation_name, tags=span_tags) as span:
                tracer.inject(span, Format.HTTP_HEADERS, headers)
                kwargs.update({'headers': headers})
                req = fn(*args, **kwargs)
                if 'code' in req.json() and req.json()['code'] not in ['0', 200]:
                    span.set_tag(tags.HTTP_STATUS_CODE, int(req.json()['code']))
                    span.set_tag(tags.ERROR, True)
                else:
                    span.set_tag(tags.HTTP_STATUS_CODE, req.status_code)
                span.log_kv({'body': req.content})
            return req
        return __decorator
    return inner


@jaeger_decorator('GET')
def get(url, params=None, headers=None, **kwargs):
    return requests.get(url, params=params, headers=headers, **kwargs)


@jaeger_decorator('POST')
def post(url, data=None, json=None, headers=None, **kwargs):
    return requests.post(url, data=data, json=json, headers=headers, **kwargs)


@jaeger_decorator('PUT')
def put(url, data=None, headers=None, **kwargs):
    return requests.put(url, data=data, headers=headers, **kwargs)


@jaeger_decorator('DELETE')
def delete(url, headers=None, **kwargs):
    return requests.delete(url, headers=headers, **kwargs)


@jaeger_decorator('PATCH')
def patch(url, data=None, headers=None, **kwargs):
    return requests.patch(url, data=data, headers=headers, **kwargs)
