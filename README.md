Сделать бэкап:
docker exec -it database pg_dump -U postgres -d '"movie-catalog"' --data-only -f /tmp/backup_utf8.sql
docker cp database:/tmp/backup_utf8.sql ./backup_final.sql

Применить бэкап:
docker cp ./backup_final.sql database:/tmp/backup_final.sql
docker exec -it database psql -U postgres -d '"movie-catalog"' -f /tmp/backup_final.sql
