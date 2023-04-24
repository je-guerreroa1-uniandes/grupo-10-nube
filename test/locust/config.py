import os

# API
G10_REVERSE_PROXY_PROTOCOL: str = os.getenv(
    'G10_REVERSE_PROXY_PROTOCOL', default='http')
G10_REVERSE_PROXY_HOST: str = os.getenv(
    'G10_REVERSE_PROXY_HOST', default='10.130.13.7')
G10_REVERSE_PROXY_PORT: str = os.getenv(
    'G10_REVERSE_PROXY_PORT', default='8888')
G10_JWT_TOKEN: str = os.getenv('G10_JWT_TOKEN', default='')

AUT_LOCATION: str = f'{G10_REVERSE_PROXY_PROTOCOL}://{G10_REVERSE_PROXY_HOST}:{G10_REVERSE_PROXY_PORT}'

# Escenario locust
G10_ESCENARIO: str = os.getenv('G10_ESCENARIO', default='3')
