from jaeger_client.config import Config
from jaeger_client.constants import TRACE_ID_HEADER as DEFAULT_TRACE_ID_HEADER
from django.conf import settings

cfg = settings.CFG
JAEGER_SERVICE_NAME = cfg.get('jaeger', 'service_name')
TRACE_ID_HEADER = 'shein-trace-id'

config = Config(config={
    'sampler': {
        'type': 'const',
        'param': 1,
    },
    'local_agent': {
        'reporting_host': cfg.get('jaeger', 'reporting_host'),
        'reporting_port': cfg.get('jaeger', 'reporting_port'),
    },
    'logging': True,
    'trace_id_header': TRACE_ID_HEADER
    },
    service_name=JAEGER_SERVICE_NAME,
    validate=True,
)

tracer = config.initialize_tracer()

__all__ = [
    "tracer"
]