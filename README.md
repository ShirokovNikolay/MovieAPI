Сделать бэкап БД:
docker exec -it database pg_dump -U postgres -d '"movie-catalog"' --data-only -f /tmp/backup_utf8.sql
docker cp database:/tmp/backup_utf8.sql ./backup.sql

Применить бэкап БД:
docker cp ./backup.sql database:/tmp/backup.sql
docker exec -it database psql -U postgres -d '"movie-catalog"' -f /tmp/backup.sql


Minio:
mc alias set myminio http://localhost:9000 admin adminadmin
mc anonymous set download myminio/movie-posters



В ссылке нужно minio заменить на localhost. Вместо header пишем то, что указали в content_type


curl.exe -X PUT "http://localhost:9000/genre-posters/tmp/genre/4e702647-dccb-4f7c-9bb3-41e7c7e22aa7_photo123.png?AWSAccessKeyId=admin&Signature=6wYwqZVd2HUPcPx2f%2F9k6KW3gUs%3D&content-type=image%2Fpng&Expires=1780331034" --data-binary "@photo123.png" -H "Content-Type: image/png"


Итог:

(
echo -ne "PUT /genre-posters/tmp/genre/40279a3b-2baf-4c36-b37b-1dff63fea25f_test.png?AWSAccessKeyId=admin&Signature=7d6A7K1P8azTtHsuTMq36AlxB%2FU%3D&content-type=image%2Fpng&Expires=1780402810 HTTP/1.1\r\n"
echo -ne "Host: minio:9000\r\n"
echo -ne "Content-Type: image/png\r\n"
echo -ne "Content-Length: $(wc -c < test.png)\r\n"
echo -ne "Connection: close\r\n\r\n"
cat test.png
sleep 1
) | nc minio 9000
