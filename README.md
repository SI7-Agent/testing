# Swagger_server

## Overview
This server was generated with the [swagger-codegen](https://github.com/swagger-api/swagger-codegen) project. By using the
[OpenAPI-Spec](https://github.com/swagger-api/swagger-core/wiki) from a remote server, you can easily generate a server stub.

This example uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

## Requirements
Python 3.8+

## Usage
To run the server, please execute the following from the root directory:

```
python3 swagger_server/__main__.py
```

and open your browser to here:

```
http://localhost:3333/api/v1/ui/
```

Your Swagger definition lives here:

```
http://localhost:3333/api/v1/swagger.json
```

ToDo:

:negative_squared_cross_mark: configure nginx    
:negative_squared_cross_mark: set up balance load    
:negative_squared_cross_mark: create beautiful (or not) web inteface app    

### Цель работы 
Создать киент-серверное приложение для разметки пользовательских изображений. В теории можно дать ему картинку, а сервис определит объекты на нем (из тех, на которые натренирована нейронная сеть).

### Функционал
 - Вход в систему
 - Выход из системы
 - Регистрация 
 - Изменение информации о себе
 - Просмотр списка фильмов
 - Поиск фильма по фильтрам
 - Просмотр информации о фильме
 - Просмотр комментариев к фильму
 - Оставить комментарий
 - Удалить комментарий
 - Поставить оценку 
 - Удалить оценку

### Usecase 
![UC1](https://github.com/SI7-Agent/web/raw/web/diags/uc1.png "Диаграмма кейсов использования 1")    
![UC2](https://github.com/SI7-Agent/web/raw/web/diags/uc2.png "Диаграмма кейсов использования 2")

### ER
![ER](https://github.com/SI7-Agent/web/raw/web/diags/er.png "Диаграмма сущностей-связей")

