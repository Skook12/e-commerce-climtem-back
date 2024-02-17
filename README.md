# e-commerce-climtem-back
---

## Docker 
**Build**
```
$ docker build -t {tag} . -f docker/Dockerfile
```
**Logs**
```
$ docker ps
$ docker logs [container_id]
```
**Run**
```
$ docker run -P {port} -d {tag}
```
```
$ docker exec -it {container_name} {op}
```
---
## Psql
**Login**
```
$psql -U postgres
```
**List databases**
```
$\l
```
**Connect database**
```
$\c {database}
```
**Show tables**
```
$\dt
```