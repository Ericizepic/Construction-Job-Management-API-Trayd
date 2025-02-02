# Construction-Job-Management-API-Trayd


This is a FastAPI project that implements a simple API to manage construction jobs and workers. Uses SQLAlchemy for database interactions. The project includes a `.env` file for environment variables.

---

## Table of Contents
1. [Installation](#installation)
2. [Setting Up the Environment](#setting-up-the-environment)
3. [Installing Requirements](#installing-requirements)
4. [Launching the API](#launching-the-api)
5. [Examples](#examples)

---

## Installation

Clone the repository:
```bash
git clone https://github.com/Ericizepic/Construction-Job-Management-API-Trayd
cd Construction-Job-Management-API-Trayd
```


## Setting Up the Environment
You will need to create a MySQL db instance. After this is done, create an .env file at the root of the directory and populate the following variables: 
``` .env
DB_USERNAME = <your username ex root>
DB_PASSWORD = <your password>
DB_HOST = <your host ex localhost>
DB_DBNAME = <your db name>
```

## Install Requirements
```bash
pip install -r requirements.txt
```


## Launching the API
To launch the API, run the following.
```bash
uvicorn main:app --reload
```


## Examples

Some examples of using the API can be found at the following Postman Collection: https://api.postman.com/collections/24746310-1b966f2a-1f7b-4acd-9a79-ad165956bd58?access_key=PMAT-01JK2YPAK3T1K5C32TW15PP3NM



