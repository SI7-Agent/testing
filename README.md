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


## Balance load testing 2:1:1 ratio

Testing configuration is    
- Flask 1.1.2 with built-in multithreaded server
- gunicorn server for pgadmin4 server-based client
- three instances of backend on 3333 (main), 4444, 5555 ports of localhost
- nginx least_conn balance algorithm

### Testing with cached static request

```
ab -n 1000000 -c 200 localhost/img/image.jpg
```

#### Balanced

- Document Path:			/img/image.jpg
- Document Length:			28989 bytes

- Concurrency Level:		200
- Time taken for tests:		99.427 seconds
- Complete requests:		1000000
- Failed requests:			0
- Non-2xx responses: 		1000000
- Total transferred:		29230000000 bytes
- HTML transferred:			28989000000 bytes
- Requests per second:		10057.62 [#/sec] (mean)
- Time per request:			19.885 [ms] (mean)
- Time per request:			0.099 [ms] (mean, across all concurrent requests)
- Transfer rate:			287093.99 [Kbytes/sec] received

Connection Times (ms)    
			  min  mean[+/-sd] median   max    
Connect:		0	 8  47.1      5    1040    
Processing:     2   12   5.8	 11      93    
Waiting:        0    6   3.9      5      82    
Total:          5   20  47.6     16    1073


#### Unbalanced

- Document Path:			/img/image.jpg
- Document Length:			28989 bytes

- Concurrency Level:		200
- Time taken for tests:		90.742 seconds
- Complete requests:		1000000
- Failed requests:			0
- Total transferred:		29230000000 bytes
- HTML transferred:			28989000000 bytes
- Requests per second:		11020.26 [#/sec] (mean)
- Time per request:			18.148 [ms] (mean)
- Time per request:			0.091 [ms] (mean, across all concurrent requests)
- Transfer rate:			314572.48 [Kbytes/sec] received

Connection Times (ms)    
			  min  mean[+/-sd] median   max    
Connect:		0	 7  44.7      5    3023    
Processing:     1   11   4.4	 10      60    
Waiting:        0    5   3.3      4      34    
Total:          5   18  45.1     16    3034


Percentage of the requests served within a certain time (ms)    
 50%      16    
 66%      17    
 75%      18    
 80%      19    
 90%      21    
 95%      25    
 98%      32    
 99%      36    
100%    3034 (longest request)


### Testing with non-static request

```
ab -n 1000000 -c 200 localhost/api/v1/human
```

#### Balanced

- Document Path:			/api/v1/human
- Document Length:			127 bytes

- Concurrency Level:		200
- Time taken for tests:		1815.222 seconds
- Complete requests:		1000000
- Failed requests:			0
- Non-2xx responses: 		1000000
- Total transferred:		335000000 bytes
- HTML transferred:			127000000 bytes
- Requests per second:		550.90 [#/sec] (mean)
- Time per request:			363.044 [ms] (mean)
- Time per request:			1.815 [ms] (mean, across all concurrent requests)
- Transfer rate:			180.23 [Kbytes/sec] received

Connection Times (ms)    
			  min  mean[+/-sd] median   max    
Connect:		0	 0   0.3      0      34    
Processing:     6  363 147.2	272    1125    
Waiting:        0  363 147.2    272    1125    
Total:          7  363 147.2    272    1125


Percentage of the requests served within a certain time (ms)    
 50%     272    
 66%     368    
 75%     520    
 80%     531    
 90%     562    
 95%     613    
 98%     701    
 99%     750    
100%    1125 (longest request)


#### Unbalanced

- Document Path:			/api/v1/human
- Document Length:			127 bytes

- Concurrency Level:		200
- Time taken for tests:		889.366 seconds
- Complete requests:		1000000
- Failed requests:			414438
    - (Connect:0, Receive:0, Length: 414438, Exceptions: 0)
- Non-2xx responses: 		1000000
- Total transferred:		331684496 bytes
- HTML transferred:			143163082 bytes
- Requests per second:		1124.40 [#/sec] (mean)
- Time per request:			177.873 [ms] (mean)
- Time per request:			0.889 [ms] (mean, across all concurrent requests)
- Transfer rate:			364.20 [Kbytes/sec] received

Connection Times (ms)    
			  min  mean[+/-sd] median   max    
Connect:		0	 2  58.3      0   15392    
Processing:     0  175 678.2	167   61029    
Waiting:        0  174 678.3    167   61029    
Total:          0  177 682.6    167   62051


Percentage of the requests served within a certain time (ms)    
 50%     167    
 66%     174    
 75%     178    
 80%     182    
 90%     221    
 95%     299    
 98%    1215    
 99%    1524    
100%   62051 (longest request)


### Testing with non-static database access request

```
ab -n 1000000 -c 200 localhost/api/v1/user/login?username=awesome_username&password=qwerty
```

#### Balanced

- Document Path:			/api/v1/user/login?username=awesome_username&password=qwerty
- Document Length:			121 bytes

- Concurrency Level:		200
- Time taken for tests:		2700.416 seconds
- Complete requests:		1000000
- Failed requests:			0
- Non-2xx responses: 		1000000
- Total transferred:		324000000 bytes
- HTML transferred:			121000000 bytes
- Requests per second:		370.31 [#/sec] (mean)
- Time per request:			540.083 [ms] (mean)
- Time per request:			2.700 [ms] (mean, across all concurrent requests)
- Transfer rate:			117.17 [Kbytes/sec] received

Connection Times (ms)    
			  min  mean[+/-sd] median   max    
Connect:		0	 0   0.4      0      58    
Processing:     9  540 222.4	424    1807    
Waiting:        0  540 222.4    424    1807    
Total:         20  540 222.4    424    1807


Percentage of the requests served within a certain time (ms)    
 50%     424    
 66%     572    
 75%     746    
 80%     781    
 90%     857    
 95%     947    
 98%    1062    
 99%    1130    
100%    1807 (longest request)


#### Unbalanced

- Document Path:			/api/v1/user/login?username=awesome_username&password=qwerty
- Document Length:			121 bytes

- Concurrency Level:		200
- Time taken for tests:		1112.423 seconds
- Complete requests:		1000000
- Failed requests:			519588
    - (Connect:0, Receive:0, Length: 519588, Exceptions: 0)
- Non-2xx responses: 		1000000
- Total transferred:		314647416 bytes
- HTML transferred:			136068052 bytes
- Requests per second:		898.94 [#/sec] (mean)
- Time per request:			222.485 [ms] (mean)
- Time per request:			1.112 [ms] (mean, across all concurrent requests)
- Transfer rate:			276.22 [Kbytes/sec] received

Connection Times (ms)    
			  min  mean[+/-sd] median   max    
Connect:		0	 3  74.6      0    7296    
Processing:     0  219 704.7	 19   61059    
Waiting:        0  219 704.7     19   61057    
Total:          0  219 713.1     20   64057


Percentage of the requests served within a certain time (ms)    
 50%      20    
 66%     238    
 75%     267    
 80%     287    
 90%     375    
 95%     570    
 98%    1471    
 99%    1778    
100%   64057 (longest request)

