"""
Application settings
"""

APP_NAME = "ClientsBackendApi"

DEBUG = True

HOST = '0.0.0.0'
PORT = 5050
PROMETHEUS_PORT = 8000
OTEL_PROTOCOL = "http"
OTEL_HOST = "nginx"
OTEL_PORT = "3600"
OTEL_PATH = "/v1/traces"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': (
                '%(asctime)s %(levelname)s %(name)s:%(funcName)s:%(lineno)d '
                '[trace_id=%(otelTraceID)s span_id=%(otelSpanID)s '
                'resource.service.name=%(otelServiceName)s] '
                '%(message)s'
            ),
        },
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(name)s:'
            '%(funcName)s:%(lineno)d - %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename':'logconfig.log',
            'maxBytes':20480,
            'backupCount': 1
        }
    },
    'loggers': {
        'FastApiBackend': {
            'handlers': ['console','file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
  'root': {
      'handlers': ['console','file'],
      'level': 'DEBUG' if DEBUG else 'INFO',
  },
}

DATABASES = {
  'local': {
    'username': 'postgres',
    'password': 'docker',
    'database': 'clients',
    'host': 'db',
    'port': 5432,
  }
}
