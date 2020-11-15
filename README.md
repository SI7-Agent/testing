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
```
[] configure nginx
[] set up balance load
[] create beautiful (or not) web inteface app
```