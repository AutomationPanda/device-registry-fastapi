# Device Registry Service (FastAPI)

This repository contains the **Device Registry Service**,
an example REST API web service for registering smart devices.
It is written in Python using [FastAPI](https://fastapi.tiangolo.com/),
and it stores data in a [TinyDB](https://tinydb.readthedocs.io/en/latest/) database (as a JSON file).
Note that it is not a "real" web service, but rather one to use as a teaching example.
This project also contains integration tests to test the REST API endpoints.

What does the Device Registry Service do?
It stores records for all smart devices a user owns in one central place.
A home could have multiple kinds of smart devices:
WiFi routers, voice assistants, thermostats, light switches, and even appliances.
This service stores information like name, location, type, model, and serial number for each device.
Its API enables callers to practice CRUD (Create, Retrieve, Update, Delete) operations.
In theory, a dashboard or monitoring app could use a registry service like this to quickly access devices.

*Note:*
This repository is the example project for Chapters 6 and 7 in Andrew Knight's book, *The Way To Test Software*.


## Installation

The Device Registry Service is designed to run on your local machine.
It should run on any operating system (Windows, macOS, Linux).
To install it:

1. Install [Python](https://www.python.org/) 3.8 or higher.
2. Clone the GitHub repository on to your local machine.
3. Install dependency packages from the command line:
   1. Change directory to the project's root directory.
   2. Run `pip install -r requirements.txt` to install all dependencies.


## Running the web service

The Device Registry Service is written using [FastAPI](https://fastapi.tiangolo.com/).
To run the web service (or "app"), run the following command:

```
uvicorn app.main:app
```

You should see output like this from the command line:

```bash
INFO:     Started server process [8846]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

When running, the web service can be accessed at `http://127.0.0.1:8000/`
(the address printed in the command's output).
If you load that address in a web browser, you should see docs for the REST API.

*Note:*
Run `uvicorn app.main:app --reload` to automatically refresh the app whenever its code is changed.


## Choosing a database

The Device Registry Service uses a [TinyDB](https://tinydb.readthedocs.io/en/latest/) database.
TinyDB is not meant to be a high-scale production database,
but it works just fine for this small example app.

TinyDB databases are stored as JSON files.
This repository comes with two TinyDB databases:

1. [`registry-dev.json`](registry-dev.json)
    * A *dev* database prepopulated with a few devices.
    * Use this one when manually poking around the app.
2. [`registry-test.json`](registry-test.json)
   * A *test* database that is empty from the start.
   * Use this one when running integration tests.

You can choose which database to use by setting the `database` property in [`config.json`](config.json).
(Read more about setting configuration options in the next section.)
The configuration defaults to the development database.
You can always discard local changes (`git restore`) to the database files to reset them.


## Configuring the web service

The Device Registry Service stores all its configuration options in [`config.json`](config.json).
The following configurations must be set in this file:

* `users`: an object of valid usernames and passwords for authentication
* `databases`: an object of available database names and their file paths
* `database`: the key for the database to use from the `databases` object
* `secret_key`: a secret key for generating JWT authentication tokens

It is recommended to use the `config.json` values provided by the repository.
However, you may change these values for added security or customization.

*Warning:*
Typically, a configuration file with secrets like these should **not** be committed to source control.
However, since this is an example project, it is committed with code for convenience.


## Reading the REST API docs

The Device Registry Service's APIs conform to the [OpenAPI Specification](https://www.openapis.org/).
FastAPI automatically generates docs at the following resource paths:

* `/docs`: The classic [Swagger UI](https://github.com/swagger-api/swagger-ui) docs
* `/redoc`: The more modern [Redoc](https://github.com/Redocly/redoc) docs

You can use these doc pages to learn how to call each endpoint.
You can also test the endpoints through the Swagger UI docs (`/docs`).

*Note:*
The home page (`/`) will redirect to the `/docs` page.


## Configuring the test cases

REST API integration tests are located in the `tests` directory.
They are written using [pytest](https://docs.pytest.org/).
The tests are not unit tests - they send requests to a live version of the Device Registry Service.
If you try to run them without the following setup steps, they will fail.

The tests require a configuration file that specifies the app's base URL and available users.
This file is located at [`tests/integration/inputs.json`](tests/integration/inputs.json).
It is a *separate* configuration file from the app's [`config.json`](config.json) file.
The following configurations must be set in this file:

* `base_url`: the base URL for the app under test
* `users`: a list of objects providing `username` and `password` values

These values should mirror the ones for the instance of the app under test.
The values provided out-of-the-box from the repository should work.

*Warning:*
Again, a configuration file like this should **not** be committed to source control.
However, since this is an example project, it is committed with code for convenience.


## Running the test cases

Once the inputs file is ready, configure the app to use the `test` database and run it.
Then, in another command line terminal, run `python -m pytest tests`.
Note that the app must be running *before* launching the tests.

Here's a condensed guide for running tests:

1. In `config.json`, set the `database` value to `test`.
2. Run `uvicorn app.main:app` from the project root directory.
3. Separately run `python -m pytest tests` from the project root directory.
