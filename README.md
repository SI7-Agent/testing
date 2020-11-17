# Swagger_server

## Overview
This server was generated with the [swagger-codegen](https://github.com/swagger-api/swagger-codegen) project. By using the
[OpenAPI-Spec](https://github.com/swagger-api/swagger-core/wiki) from a remote server, you can easily generate a server stub.

This example uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

## Requirements
- Python 3 with list of modules in requirements.txt
- Cuda 10.1 libs
- PostgreSQL with server-based pgadmin4 on 5050 port 
- Linux (if you want nginx support else you have to adapt it for other OS)

## Usage
Run pgadmin4 as service with gunicorn (--chdir <your_path_to_installed_pgadmin>)

```
sudo gunicorn --bind unix:/tmp/pgadmin4.sock
			  --workers=1
			  --threads=25
			  --chdir lib/python2.7/site-packages/pgadmin4
			  pgAdmin4:app
```

To run the server, please execute the following from the project root directory (by default runs at 3333 port):

```
python3 swagger_server/__main__.py [port]
```

and open your browser to here:

```
http://localhost:port/ui/    
http://localhost/api/v1/ui/ (with nginx)
```

Your Swagger definition lives here:

```
http://localhost:port/swagger.json    
http://localhost/api/v1 (with nginx)
```

### ToDo:

:white_check_mark: configure nginx    
:white_check_mark: set up balance load    
:negative_squared_cross_mark: create beautiful (or not) web inteface app    

### Цель работы 
Создать киент-серверное приложение для разметки пользовательских изображений. В теории можно дать ему картинку, а сервис определит объекты на нем (из тех, на которые натренирована нейронная сеть).

### Функционал
- Вход в систему :heavy_check_mark:
- Выход из системы :heavy_check_mark:
- Регистрация :heavy_check_mark:
- Определение человека на изображении
    - Определение лица :heavy_check_mark:
    - Распознание эмоций 
        - Эмоция злости :angry: :heavy_check_mark:
        - Эмоция грусти :cry: :heavy_check_mark:
        - Эмоция удивления :astonished: :heavy_check_mark:
        - Эмоция страха :fearful: :heavy_check_mark:
        - Эмоция счастья :smile: :heavy_check_mark:
        - Эмоция отвращения :worried: :heavy_check_mark:
        - Эмоция нейтральности :neutral_face: :heavy_check_mark:
    - Определение пола
        - Мужской пол :man: :heavy_check_mark:
        - Женский пол :woman: :heavy_check_mark:
- Определение объекта на изображении
    - Фон :black_large_square: :heavy_exclamation_mark:
    - Аэроплан :airplane: :heavy_exclamation_mark:
    - Велосипед :bicyclist: :heavy_check_mark:
    - Птица :bird: :heavy_exclamation_mark:
    - Лодка :boat: :heavy_check_mark:
    - Бутылка :baby_bottle: :heavy_check_mark:
    - Автобус :bus: :heavy_exclamation_mark:
    - Автомобиль :car: :heavy_check_mark:
    - Кошка :cat: :heavy_check_mark:
    - Стул 🪑 :heavy_check_mark:
    - Корова :cow: :heavy_exclamation_mark:
    - Обеденный стол 🍽 :heavy_check_mark:
    - Собака :dog: :heavy_check_mark:
    - Лошадь :horse: :heavy_exclamation_mark:
    - Мотоцикл :bike: :heavy_check_mark:
    - Растение в горшке :four_leaf_clover: :heavy_check_mark:
    - Овца :sheep: :heavy_exclamation_mark:
    - Диван 🛋 :heavy_check_mark:
    - Поезд :train: :heavy_exclamation_mark:
    - Телеэкран :tv: :heavy_check_mark:		
- Применение выборочных фильтров к изображению :heavy_check_mark:

:heavy_check_mark: - протестировано и гарантировано работает    
:heavy_exclamation_mark: - работает, но не гарантировано 


### Usecase 
![UC1](https://github.com/SI7-Agent/web/raw/web/diags/uc1.png "Диаграмма кейсов использования 1")    
![UC2](https://github.com/SI7-Agent/web/raw/web/diags/uc2.png "Диаграмма кейсов использования 2")

### ER
![ER](https://github.com/SI7-Agent/web/raw/web/diags/er.png "Диаграмма сущностей-связей")

