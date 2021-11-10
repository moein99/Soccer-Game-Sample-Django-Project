# Soccer Game

## Sections
1. [Endpoints](#endpoints)
2. [Run the project in a virtual environment](#run-the-project-in-a-virtual-environment) 
3. [Run the project using docker-compose](#run-the-project-using-docker-compose) 

### Endpoints:
1. Register  
```
POST /api/register
data:
{
    "email": "xxx",
    "password": "xxx",
    "repeated_password": "xxx",
    "team_name": "xxx",
    "team_country": "xxx"
}
```
2. Login  
Returns a session and a timeout which indicates the amount of time that session will be valid. Session id should be in headers for other APIs. For all APIs other than **register** and **login**, session header is required.
```
POST /api/login
data:
{
    "email": "xxx",
    "password": "xxx"
}
```
3. Team   
GET returns user's team information.  
PUT updates user's team information.
```
GET /api/team
headers:
{
    "session": "xxx"
}

PUT /api/team
data: 
{
    "name": "new name",
    "country: "new country"
}
```
4. Players  
GET returns list of players in user's team.  
PUT updates a player's information.
```
GET /api/players

PUT /api/players/<identifier>
data:
{
    "first_name": "new first name",
    "last_name": "new last name",
    "country": "new country name",
}
```
5. Transfer  
GET returns transfer list.  
POST creates a transfer record for a player.  
PUT updates a transfer record for a player. (change the price)
```
GET /api/transfer

POST /api/transfer
data: 
{
    "player_identifier": "xxx",
    "price": integer_value
}

PUT /api/transfer/<player_identifier>
data: 
{
    "price": integer_value
}
```
6. Buy  
Moves a player to user's team and updates the balances of teams and the player's market value.
```
POST /api/buy
data: 
{
    "player_identifier": "xxx"
}
```

### Run the project in a virtual environment
0. Befure moving on, you need to have a redis-server up and running in your machine. You can change host, port and db in the settings file. Use [this](https://redis.io/topics/quickstart) link for installing Redis.
1. Make a virtual environment
```shell
python3 -m virtualenv .venv
```
2. Activate it
```shell
source .venv/bin/activate
```
3. Install the requirements
```shell
pip install -r requirements.txt
```
4. Migrate!
```shell
python3 manage.py migrate
```
5. Run server or tests
```shell
python3 manage.py runserver
python3 manage.py test
```

### Run the project using docker-compose
Make sure you have **docker** and **docker-compose** already installed on your machine
```shell
docker-compose up
```