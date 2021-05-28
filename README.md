# shein-django-jaeger-middleware
shein 运维开发部专用的django jeager middleware

## Installing
```bash
$ pip install shein-django-jaeger-middleware
```

将 ```shein_django_jaeger_middleware.middleware.JaegerMiddleWare```
添加到`setting.py`文件的`MIDDLEWARE`中

例如:
```
MIDDLEWARE = [
	...
	'shein_django_jaeger_middleware.middleware.JaegerMiddleWare'
]
```

在配置文件中cfg.ini中添加配置信息
```
[jaeger]
service_name = your_service
reporting_host = your_jaeger_ip
reporting_port = your_jaeger_udp_port
```

## Getting Started
从shein_django_jaeger_middleware引入requests，如原requests库一样使用
```python
from shein_django_jaeger_middleware import requests

req = requests.get(url, headers=headers)
```

## Enjoy!
如有问题请联系我：[zhpan188@gmail.com](zhpan188@gmial.com)