# Construction-Job-Management-API-Trayd


This is a FastAPI project that implements a simple API to manage construction jobs and workers. Uses SQLAlchemy for database interactions. The project includes a `.env` file for environment variables.

---

## Table of Contents
1. [Installation](#installation)
2. [Setting Up the Environment](#setting-up-the-environment)
3. [Installing Requirements](#installing-requirements)
4. [Launching the API](#launching-the-api)
5. [Setting Up the Database Table](#setting-up-the-database-table)

---

## Installation

Clone the repository:
```bash
git clone https://github.com/Ericizepic/Construction-Job-Management-API-Trayd
cd Construction-Job-Management-API-Trayd
```


## Setting Up the Environment

Create an .env file at the root of the directory and populate the following variables: 
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

```bash
uvicorn main:app --reload
```