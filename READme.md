# Travel App api

#pre-requisites

- **docker**
- **docker-compose**
- **pipenv**
- **python 3.10**
- **postgresql**
- **django**
- **djangorestframework**
- **git**
- **pip**

you canb verify versions of all the above packages by running the following command

```sh
git --version
docker --version
docker-compose --version
pipenv --version
python --version

```

## Project Structure

- **travel_api**
- **travel_app**
- **docker-compose.yml**
- **Dockerfile**
- **Pipfile**
- **Pipfile.lock**
- **README.md**
- **manage.py**

# Endpoints

- refer to collection of endpoints in the **Travel_app.postman_collection.json** file, can be imported to postman

- **destinations**

  - this endpoint will return a list of destinations based on the search query
  - the search query should be a string
  - the response should be a list of destinations
  - if no destinations are found, the response should be an empty list
  - if an error occurs, the response should be a json object with a message key and the error message

- **weather**

  - this endpoint will return the weather for a given location
  - the location should be a json object with latitude and longitude keys
  - the response should be a json object with weather information
  - if an error occurs, the response should be a json object with a message key and the error message

- **itineraries**

  - this endpoint will create an itinerary for a given location
  - the location should be a json object with destination and weather information

- **activities**
  - this endpoint will create an activity for a given itinerary

# set up with docker

1. clone the repository

   ```sh
   git clone https://github.com/madimetja/travel_app.git
   ```

2. using pipenv, install the dependencies

   ```sh
    pip install pipenv
    cd travel_app

    pipenv install

    python manage.py runserver
   ```

3. cd into the project directory

   ````sh
       cd travel_app

       create .env file from env.template

       docker-compose -f ./docker-compose.yml up --build

       create credentials for postgres
       create database travel_app within postgres

       docker-compose up
       ```
   ````
