# Cloud Layer - Backend
## Author
Done by: Sherman Ng Wei Sheng

## Requirements
<u>Tested on the following hardware / software</u>: <br/>
Device: Windows 10, 64 bit<br/>
Python Version: 3.10.2
Hosted On: Koyeb

## Hosted Links
Host URL: https://prediction-iht-cloud-backend.koyeb.app/
Cloud DB Hosted On: Aiven

## Directory Description
1. `app.py`: The flask app that act as backend server
2. `database.py`: The module to connect with cloud database
3. `model.py`: Regression model for predicting consumed time
4. `Procfile`: Contains command to run the app
5. `requirements.txt`: Necessary Python packages

## How to Run
1. Start MQTT Broker using the `emqx` image
```bash
docker-compose up
```