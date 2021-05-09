
<h1 align="center"> 
   BotTrading :robot:
</h1>



![Python](https://img.shields.io/badge/Python-v3.9.3-blue) 


## How to run this project local

- NOTE: Commands for installation on Linux, it is necessary to have the [virtualenv](https://docs.python.org/3/tutorial/venv.html) installed and configured.


|           Description                |                          COMMANDS                                      |  
|--------------------------------------|------------------------------------------------------------------------|
|  Clone the repository                |  `git clone git@github.com:fabriciocovalesci/BotTrading.git`           |   
|  Access the BotTrading folder        |  `cd BotTrading`                                                       |   
|  Create a python virtualenv          |  `python -m venv virtualenv`                                           |   
|  Enable virtualenv                   |  `source virtualenv/bin/activate`                                      |   
|  Install project dependencies        |  `pip install -r requirements.txt`                                     |  


### Create `.env` at the root of the project

```
API_KEY = 'YOUR_API_KEY_BINANCE'
API_SECRET = 'YOUR_API_SECRET_BINANCE'
GMAIL_EMAIL = 'YOUR_EMAIL'
GMAIL_PASSWORD = 'YOUR_PASSWORD'
GMAIL_RECEIVER_ADDRESS = 'YOUR_EMAIL_OR_OTHER_EMAIL'
POSTGRESQL_USER = 'USER_POSTGRESQL'
POSTGRESQL_PASSWORD = 'PASSWORD_POSTGRESQL'
POSTGRESQL_DATABASE = 'NAME_DATA_BASE'
POSTGRESQL_HOST = '127.0.0.1'
POSTGRESQL_PORT = '5432'
```

### Now run **BotTrading**

```

>> python3 Bot.py

```
