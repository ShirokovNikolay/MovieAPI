Сделать бэкап БД:
docker exec -it database pg_dump -U postgres -d '"movie-catalog"' --data-only -f /tmp/backup_utf8.sql
docker cp database:/tmp/backup_utf8.sql ./backup.sql

Применить бэкап БД:
docker cp ./backup.sql database:/tmp/backup.sql
docker exec -it database psql -U postgres -d '"movie-catalog"' -f /tmp/backup.sql


Minio:
mc alias set myminio http://localhost:9000 admin adminadmin
mc anonymous set download myminio/имя_бакета



curl.exe -X PUT "http://localhost:9000/genre-posters/tmp/genre/e882ea68-09ac-4a25-bb9a-21e74f12a122_photo123.png?AWSAccessKeyId=admin&Signature=HyH%2B5sul0ZkNohUo0pPLonhE9%2FY%3D&content-type=image%2Fpng&Expires=1780329148" --data-binary "@photo123.png" -H "Content-Type: image/png"




В ссылке нужно minio заменить на localhost. Вместо header пишем то, что указали в content_type


curl.exe -X PUT "http://localhost:9000/genre-posters/tmp/genre/4e702647-dccb-4f7c-9bb3-41e7c7e22aa7_photo123.png?AWSAccessKeyId=admin&Signature=6wYwqZVd2HUPcPx2f%2F9k6KW3gUs%3D&content-type=image%2Fpng&Expires=1780331034" --data-binary "@photo123.png" -H "Content-Type: image/png"
