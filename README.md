Сделать бэкап:
docker exec -it database pg_dump -U postgres -d '"movie-catalog"' --data-only -f /tmp/backup_utf8.sql
docker cp database:/tmp/backup_utf8.sql ./backup.sql

Применить бэкап:
docker cp ./backup.sql database:/tmp/backup.sql
docker exec -it database psql -U postgres -d '"movie-catalog"' -f /tmp/backup.sql
