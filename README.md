# Cloud Layer - Backend
## Author
Done by: Sherman Ng Wei Sheng

## Requirements
<u>Tested on the following hardware / software</u>: <br/>
Device: Windows 10, 64 bit<br/>
Python Version: 3.10.2 <br/>
Hosted On: Koyeb

## Hosted Links
Host URL: https://prediction-iht-cloud-backend.koyeb.app/ <br/>
Cloud DB Hosted On: Aiven

## Directory Description
1. `app.py`: The flask app that act as backend server
2. `database.py`: The module to connect with cloud database
3. `model.py`: Regression model for predicting consumed time
4. `Procfile`: Contains command to run the app
5. `requirements.txt`: Necessary Python packages

## How to Run
1. Update the following environment variables in a `.env` file
```
DB_USER=\<remote pgsql database username>
DB_PASSWORD=\<remote pgsql password>
DB_HOST=\<remote pgsql ip address>
DB_PORT=\<remote pgsql port number>
DB_DATABASE=\<remote pgsql database name>
```
2. Install all dependencies
```bash
pip install -r requirements.txt
```
3. Start the express server by running
```bash
python app.py
```

## Note
For this project, the cloud db instance, as provided in the `.env` file, has been set up to do a logical replication of the fog layer db.
