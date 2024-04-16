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
**Delete PSQL data**
```
$ docker volume ls
```
```
$ docker volume prune
```
```
$ docker volume rm project_pgdata
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