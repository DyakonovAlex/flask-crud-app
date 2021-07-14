# flask-crud-app

Это пример простого веб-приложения CRUD, с настроенным деплоем в [Heroku](https://signup.heroku.com/)

## Deployment to Heroku

Установить [Heroku Command-Line Interface (CLI)](https://devcenter.heroku.com/articles/heroku-cli)

После установки

```bash
$ heroku login
``` 

В файле Procfile указано как запускать приложение.  
Дальше необходимо создать приложение в Heroku. Поскольку имена приложений в Heroku должны быть уникальными, вам нужно будет выбрать другое имя.

```bash
$ heroku create flask-crud-app
```

Теперь запускаем процесс сборки и развертывания:

```bash
$ git push heroku master
```

Чтобы открыть URL-адрес вашего приложения:

```bash
$ heroku open
```

## Implementing the Deployment Workflow in Heroku

Для организации pipeline нужно сделать два шага:

1. Создать различных приложений для среды staging и среды production
2. Сделать эти приложения частью одного pipeline

```bash
$ heroku create flask-crud-app-staging --remote staging
$ git push staging master
```

Теперь у нас есть два приложения Heroku. Сделаем Heroku pipeline и добавим production:

```bash
$ heroku pipelines:create flask-crud-app-pipe \
--app flask-crud-app --stage production
```

Выполните следующую команду, чтобы проассоциировать приложение с именем prod

```bash
$ heroku git:remote --app flask-crud-app --remote prod
```

Добавим в Heroku pipeline и добавим staging:

```bash
$ heroku pipelines:add flask-crud-app-pipe \
--app flask-crud-app-staging --stage staging
```

Для деплоя на prod той же версии, что сейчас задеплоена на staging:

```bash
$ heroku pipelines:promote --remote staging
```

Установка переменных окружения:

```bash
$ heroku config:set --remote staging \
SECRET_KEY=the-staging-key \
APP_SETTINGS=config.StagingConfig

$ heroku config:set --remote prod \
SECRET_KEY=the-production-key \
APP_SETTINGS=config.ProductionConfig
```