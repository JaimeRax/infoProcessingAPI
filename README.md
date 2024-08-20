
# Information Processing API

![Python](https://img.shields.io/badge/Python-3.10.6-blue.svg)

This API works for the processing of Finanssoreal information. Such as character extraction from images, face comparison, numerical analysis, etc.


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
Install librery tesseract for python

```bash
  pip install pytesseract
```

Install all libraries and dependencies

```bash
  python -m pip install -r requirements.txt
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
`STORAGE_ROUTE=name_route`
`STORAGE_ROUTE_BD=name_route`


## Run Locally

With the virtual environment initialized, run:

```bash
  python main.py
```


## API Reference

#### Get response of facial recognition and comparison

```http
  GET /facial_recognition
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `first_image` | `media` | **Required**. First image to compare |
| `second_image` | `media` | **Required**. Second image to compare |

