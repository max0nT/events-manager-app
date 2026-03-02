# events-manager-app

Short description: easy-to-use application fro event management

## Key features

- Easy-to-use both events and places API
- Email sending about coming events
- Sync weather data with event start, thanks for [Open meteo](https://open-meteo.com/) who provides free API for that.
- Import/Export events data

## Tools to use

- [uv](https://docs.astral.sh/uv/)
- [docker](https://www.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)

## Local installation

- Insert following lines in your `/etc/hosts` file
```bash
127.0.0.1 redis
127.0.0.1 postgres
127.0.0.1 mailpit
127.0.0.1 weather
```
- Copy local settings
```bash
cp .env.example .env
```
- Then install virtual environment
```bash
uv sync --all-groups  && source .venv/bin/activate
```
- After that, you need to setup docker-compose services(db's)
```bash
docker compose up -d postgres redis mailpit dozzle
```
- Note, if you wanna run app by using only docker services, you don't have to specify services to run from command above

- Finally, to run REST API on django
```bash
python manage.py runserver
```
- In another console run weather sync api
```bash
python -m weather.app
```

## Enhancements for app
- Add tests via pytest
- Add support s3(minIO)
