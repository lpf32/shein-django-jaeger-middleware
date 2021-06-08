import requests
from opentracing.ext import tags
from opentracing import Format

from . import tracer


def jaeger_decorator(method):
    def inner(fn):
        def __decorator(*args, **kwargs):
            if 'url' in kwargs:
                url = kwargs.get('url')
            else:
                url = args[0]
            span_tags = {tags.HTTP_METHOD: method, tags.HTTP_URL: url, tags.SPAN_KIND: tags.SPAN_KIND_RPC_CLIENT}
            if 'headers' in kwargs:
                headers = kwargs.get('headers')
            else:
                headers = {}
            operation_name = 'outbound-{}'.format(url)
            with tracer.start_span(operation_name=operation_name, tags=span_tags) as span:
                tracer.inject(span, Format.HTTP_HEADERS, headers)
                kwargs.update({'headers': headers})
                req = fn(*args, **kwargs)
                result = req.json()
                if 'code' in result and result['code'] not in ['0', 200]:
                    span.set_tag(tags.HTTP_STATUS_CODE, int(result['code']))
                    span.set_tag(tags.ERROR, True)
                else:
                    span.set_tag(tags.HTTP_STATUS_CODE, req.status_code)
                span.log_kv({'body': result})
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


def request(method, url, **kwargs):
    method = str.lower(method)
    if method == 'get':
        req = get(url, **kwargs)
    elif method == 'put':
        req = put(url, **kwargs)
    elif method == 'post':
        req = post(url, **kwargs)
    elif method == 'delete':
        req = delete(url, **kwargs)
    elif method == 'patch':
        req = patch(url, **kwargs)
    else:
        return ValueError('Unknown HTTP Method: {}'.format(method))
    return req
