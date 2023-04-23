# Usando Apache HTTP server benchmarking tool

```bash
# Escenario 1: API Login
ab -n 1000 -c 100 -p ./test_data.json -e report.csv -T application/json -rk http://127.0.0.1:3000/api/auth/login

# Escenario 2: API Tareas por usuario
ab -n 1000 -c 100 -H 'Authorization: Token eyCs' -e report.csv -T application/json -rk http://127.0.0.1:3000/api/tasks\?max\=3\&order\=1
```