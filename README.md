# work
установить необходимые библиотеки. Используйте следующую команду:
   pip install Flask psycopg2 elasticsearch
   Настройте PostgreSQL:
   - Убедитесь, что PostgreSQL установлен и запущен.
   - Создайте базу данных и таблицу для хранения документов
          CREATE DATABASE yourdbname;
     CREATE TABLE documents (
         id SERIAL PRIMARY KEY,
         title TEXT NOT NULL,
         content TEXT NOT NULL
     );
     
Настройте Elasticsearch:

   - Убедитесь, что Elasticsearch установлен и запущен.
   - Проверьте, что Elasticsearch работает, открыв в браузере
          http://localhost:9200
     
Настройте переменные подключения:

   Измените переменные подключения к базе данных в коде:
      dbname='yourdbname',  # название вашей базы данных
   user='youruser',  # ваш пользователь PostgreSQL
   password='yourpassword',  # ваш пароль PostgreSQL
   host='localhost',
   port='5432'
   

   
