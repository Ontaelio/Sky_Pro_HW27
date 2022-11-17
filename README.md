*Домашка 28*

https://skyengpublic.notion.site/28-Postgres-relations-QuerySet-7a440f26dd914d67ab788093f5a158e3
 
1) Запуск csv2json.py конвертирует CSV фалы в JSON фикстуры.
2) Накатить миграции, а затем наполнить базу:
* python python manage.py loaddata ad.json category.json location.json user.json

В качестве many2many таблицы добавлена модель тэгов. Отдельных вьюшек для них нет, но по ним можно вызывать объясления - ad/?tag=...

Также тэги можно прописывать через метод PATCH объявлений. Если передать поле 'tags', тэги заменятся на новые (или затрутся, если []).
