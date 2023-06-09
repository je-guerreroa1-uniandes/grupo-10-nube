import os

# Flask
PORT: int = int(os.getenv('PORT', default='5000'))
USING_APP_ENGINE: bool = os.getenv('GAE_ENV', default=None) is not None

# Database (PostgreSQL)
G10_DB_PREFIX: str = os.getenv('G10_DB_PREFIX', default='postgresql')
G10_DB_USERNAME: str = os.getenv('G10_DB_USERNAME', default='converter_db')
G10_DB_PASSWORD: str = os.getenv(
    'G10_DB_PASSWORD', default='ckhAMLIteFlYheRptAteapeze')
G10_DB_HOST: str = os.getenv('G10_DB_HOST', default='10.93.240.3')
G10_DB_PORT: str = os.getenv('G10_DB_PORT', default='5432')
G10_DB_DBNAME: str = os.getenv('G10_DB_DBNAME', default='conversion')

POSTGRES_URI: str = f"{G10_DB_PREFIX}://{G10_DB_USERNAME}:{G10_DB_PASSWORD}@{G10_DB_HOST}:{G10_DB_PORT}/{G10_DB_DBNAME}"

# Redis
G10_REDIS_PREFIX: str = os.getenv('G10_REDIS_PREFIX', default='redis')
G10_REDIS_PASSWORD: str = os.getenv(
    'G10_REDIS_PASSWORD', default='lOGleSPirDOLEYsiceWlemPtO')
G10_REDIS_HOST: str = os.getenv('G10_REDIS_HOST', default='10.130.13.4')
G10_REDIS_PORT: str = os.getenv('G10_REDIS_PORT', default='6379')
G10_REDIS_DBNAME: str = os.getenv('G10_REDIS_DBNAME', default='0')

REDIS_URI: str = f"{G10_REDIS_PREFIX}://:{G10_REDIS_PASSWORD}@{G10_REDIS_HOST}:{G10_REDIS_PORT}/{G10_REDIS_DBNAME}"

# JWT
G10_JWT_SECRET: str = os.getenv(
    'G10_JWT_SECRET', default='frase-secreta-grupo-10-nube')

GOOGLE_PUBSUB_PROJECT_ID = 'uniandes-grupo-10'
GOOGLE_PUBSUB_TOPIC_NAME = 'api-worker'
GOOGLE_PUBSUB_TOPIC_PATH = f'projects/{GOOGLE_PUBSUB_PROJECT_ID}/topics/api-worker'
GOOGLE_PUBSUB_SUBSCRIPTION_ID = 'api-worker-sub'

# Cloud storage
G10_CLOUD_BUCKET: str = os.getenv('G10_CLOUD_BUCKET', default='uniandes-grupo-10.appspot.com')

# Path to your service account key file
G10_SERVICE_ACCOUNT_KEY_PATH = './google-json/uniandes-grupo-10-9a07a80edaf8.json'
