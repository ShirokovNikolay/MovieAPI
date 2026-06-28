Quick start

Configure minio:
```bash
docker exec -it minio mc alias set myminio http://localhost:9000 admin adminadmin
docker exec -it minio mc mb myminio/genre-posters --ignore-existing
docker exec -it minio mc mb myminio/movie-posters --ignore-existing
docker exec -it minio mc mb myminio/movies --ignore-existing
docker exec -it minio mc anonymous set download myminio/genre-posters
docker exec -it minio  mc anonymous set download myminio/movie-posters
docker exec -it minio  mc anonymous set download myminio/movies
```


Start app first time:
```bash
docker compose build; docker compose up --watch
```


Build app:
```bash
docker compose build
```

Run app:
```bash
docker compose up --watch
```

Backup database:
```bash
docker exec -it database pg_dump -U postgres -d '"movie-catalog"' --data-only -f /tmp/backup_utf8.sql
docker cp database:/tmp/backup_utf8.sql ./backup.sql
```

```bash
docker cp ./backup.sql database:/tmp/backup.sql
docker exec -it database psql -U postgres -d '"movie-catalog"' -f /tmp/backup.sql
```
