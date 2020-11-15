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

