# Information Processing API

![Python](https://img.shields.io/badge/Python-3.10.6-blue.svg)


## Installation

Create a python virtual environment in the main project folder.

```bash
  python3 -m venv venv
```

Run the virtual environment.

- Windows (PowerShell)
```bash
  venv\Scripts\activate
```

- Linux
```bash
  source venv/bin/activate
```

Install all libraries and dependencies

```bash
  python3 -m pip install -r requirements.txt
```

Check the Installation

```bash
  pip freeze
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file in the main project directory.

`PROJECT_NAME='INFO_PROCESSING_API'`  
`DB_ENGINE='django.db.backends.mysql'`  
`DB_NAME='db_name'`  
`DB_USER='db_user'`  
`DB_PASS='db_pass'`  
`DB_HOST='127.0.0.1'`  
`DB_PORT=3306`  
`STORAGE_ROUTE='path_name_route'`
`STORAGE_ROUTE_BD='path_name_route'`


## Run Locally

With the virtual environment initialized, run:

```bash
  python3 main.py
```
