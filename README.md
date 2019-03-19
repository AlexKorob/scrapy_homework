## Scrapy

Scrape barneywarehouse.com

#### Prepare project:

```bash
  git clone https://github.com/AlexKorob/scrapy_homework.git
  cd scrapy_homework
  python3 -m venv ./venv
  . venv/bin/activate
  pip3 install -r requirements.txt
```

#### Configure Postgresql:

```bash
  sudo su - postgres
  psql
  CREATE DATABASE warehouse;
  CREATE USER alex WITH PASSWORD '123';
  GRANT ALL PRIVILEGES ON DATABASE warehouse TO alex;
  \q
  logout
```

#### Run Spider:

```bash
  cd ./warehouse
  scrapy crawl warehouse
```

#### Run Celery:

```bash
  cd ../parsing_site
  celery -A my_site worker -l info
```

#### Start site:

```bash
  ./manage.py migrate my_site
  ./manage.py runserver
```
Then go to https://localhost:8000/index/ on your browser
