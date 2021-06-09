from django.http import HttpRequest, HttpResponse
from opentracing import Format
from opentracing.ext import tags
import json

from . import tracer, TRACE_ID_HEADER


class JaegerMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
        span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER, tags.HTTP_URL: request.path,
                     tags.HTTP_METHOD: request.method
                     }
        operation_name = 'inbound-{}'.format(request.path)
        with tracer.start_active_span(operation_name=operation_name, child_of=span_ctx, tags=span_tags) as scope:
            tracer.inject(scope.span, Format.HTTP_HEADERS, request.META)
            response = self.get_response(request)
            response[TRACE_ID_HEADER] = request.META.get(TRACE_ID_HEADER, "")

            content = json.loads(getattr(response, 'content', '{}'))
            if 'code' in content and content['code'] not in ['0', 200]:
                scope.span.set_tag(tags.HTTP_STATUS_CODE, int(content['code']))
                scope.span.set_tag(tags.ERROR, True)
            else:
                scope.span.set_tag(tags.HTTP_STATUS_CODE, response.status_code)
            scope.span.log_kv({'body': content})
        return response

