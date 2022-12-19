# device-registry-fastapi

To run the app:

```
uvicorn app.main:app --reload
```


# Old README

# device-registry

This project is the **Device Registry Service**,
an example REST API web service for registering smart devices.
It is written in Python using Flask, and it stores data in a SQLite database.
Note that it is not a "real" web service, but rather one to use as a teaching example.
This project also contains integration tests to test the REST API endpoints.

What does the Device Registry Service do?
It stores records for all smart devices a user owns in one central place.
A home could have multiple kinds of smart devices:
WiFi routers, voice assistants, thermostats, light switches, and even appliances.
This service stores information like name, location, type, model, and serial number for each device.
Its API enables callers to practice CRUD (Create, Retrieve, Update, Delete) operations.
In theory, a dashboard or monitoring app could use a registry service like this to quickly access devices.


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

The Device Registry Service is written using [Flask](https://flask.palletsprojects.com/en/2.0.x/).
Before running it from the command line,
set the `FLASK_APP` environment variable to the name of the app's main module, `registry`.

* Windows: `set FLASK_APP=registry`
* macOS and Linux: `export FLASK_APP=registry`

To run the web service, run `flask run`.
You should see output like this from the command line:

```bash
$ flask run
 * Serving Flask app 'registry' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

When running, the web service can be accessed at `http://127.0.0.1:5000/`
(the address printed by the `flask run` output).
If you load that address in a web browser, you should see docs for the REST API.


## Choosing a database

Out of the box, the Device Registry Service uses a [SQLite](https://www.sqlite.org/index.html) database.
SQLite is not meant to be a high-scale production database,
but it works just fine for this small example web service.

There are two ways to manage the app's database:

1. *Testing:* create a fresh, empty, in-memory SQLite database every time `flask run` is launched.
2. *Development:* create a SQLite database file named `registry_data.sqlite` with a few prepopulated devices.

Set the `FLASK_CONFIG` environment variable to chose which database to use:

1. For the *Testing* database, set `FLASK_CONFIG` to `testing`.
2. For the *Development* database, set `FLASK_CONFIG` to `development`.

If `FLASK_CONFIG` is not set, then the app uses the *Testing* database by default.

If you want to use the *Development* database,
you must create it *before* running the Flask app.
Run `flask init-db` to create the initial `registry_data.sqlite` file in the project's root directory.
Then, set `FLASK_CONFIG` to `development` and run `flask run` to run the app with this database.
Any changes will persist, even after the app is restarted.


## Setting configuration options

The Device Registry Service stores all its configuration options in `config.py`.
The following configuration options have default values,
but they may optionally be overridden using environment variables:

* `SECRET_KEY`: the secret key used for app security
* `AUTH_USERNAME1`: the username for user 1
* `AUTH_PASSWORD1`: the password for user 1
* `AUTH_USERNAME2`: the username for user 2
* `AUTH_PASSWORD2`: the password for user 2
* `AUTH_TOKEN_EXPIRATION`: the expiration time in seconds for authentication tokens

***Warning:*** Overriding these options is not recommended for most cases.


## Reading the REST API docs

The Device Registry Service provides its REST API docs at the `/docs/` resource.
The home page `/` also redirects to the `/docs/` page.
The `/docs/json/` resource provides the docs as a JSON object.
Docs are automatically generated using [flask-selfdoc](https://github.com/jwg4/flask-selfdoc).


## Running the test cases

REST API integration tests are located in the `tests` directory.
They are written using [pytest](https://docs.pytest.org/).
The tests are not unit tests -
they send requests to a live version of the Device Registry Service.
If you try to run them without the following setup steps, they will fail.

The tests require a configuration file that specifies the web service's base URL and available users.
In the `tests/integration` directory, create a file named `inputs.json` with the following contents:

```json
{
  "base_url": "<base-url>",
  
  "users" : [
    {
      "username": "<user1-username>",
      "password": "<user1-password>"
    },
    {
      "username": "<user2-username>",
      "password": "<user2-password>"
    }
  ]
}
```

You will need to substitute appropriate values for the `"<...>"` values.
If you run the Device Registry Service with the default values from `config.py`,
then `tests/integration/inputs.json` should look like this:

```json
{
  "base_url": "http://127.0.0.1:5000",
  
  "users" : [
    {
      "username": "pythonista",
      "password": "I<3testing"
    },
    {
      "username": "engineer",
      "password": "Muh5devices"
    }
  ]
}
```

***Note:*** `tests/integration/inputs.json` is not committed to the repository
because inputs and secrets should *never* be committed to a publicly-shared location.
(Nevertheless, this web service is a teaching example,
so values are pasted in the section above for convenience and clarity.)

Once the inputs file is ready, configure the app to use the *Testing* database and run `flask run`.
Then, in another command line terminal, run `python -m pytest tests`.
Note that the web app must be running *before* launching the tests.

Here's a condensed guide for running tests:

1. Set the `FLASK_APP` environment variable to `registry`.
2. Set the `FLASK_CONFIG` environment variable to `testing`.
3. Run `flask run` from the project root directory.
4. Create the `tests/integration/inputs.json` file.
5. Run `python -m pytest tests` from the project root directory.


## Test Outline

***Remove this section upon chapter completion.***

1. Basic request-response-validate test for '/status/'
   * Set up project
   * Write the test with hard-coding
   * Improve with inputs file and base URL builder
2. Authentication for '/devices/'
   * Demonstrate GET with and without auth & explain
   * Add credentials to inputs file
   * Write positive test with auth
   * Write negative test without auth
   * Show auth with tokens
   * Show how to reuse token
   * Discuss if every endpoint should test every type of auth or no-auth
3. CRUD tests with '/devices/<id>'
   * Include negative cases
4. Testing multiple objects with '/devices/'
   * Creating and deleting multiple objects
   * Query parameters for large data
5. Authorization tests with '/devices/'
   * Multiple users
   * Multiple methods
6. Additional REST API factors
   * File downloads
   * HEAD and OPTIONS for GET
   * Invalid methods
