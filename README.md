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
	'django_jaeger_middleware.middleware.JaegerMiddleWare'
]
```

## Enjoy!
如有问题请联系我：[zhpan188@gmail.com](zhpan188@gmial.com)