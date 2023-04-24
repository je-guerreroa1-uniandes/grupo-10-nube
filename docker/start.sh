if [ -f custom-locust.env ]; then
    # Solo la variable de entorno G10_JWT_TOKEN
    eval $(cat custom-locust.env | grep '^G10_JWT_TOKEN' | awk '{print "export " $0}')
fi
docker compose --file docker-compose.dev.yml up -d --build --remove-orphans