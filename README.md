# Steps to setup the project :

- Clone the repositoriy with :
`git clone https://github.com/akashaviator/LuckyDrawRaffle.git`

- Then: `cd LuckyDrawRaffle`

- Make sure you have python 3.6+ installed.

- If you're usign Linux activate the virtual environment with `source env/bin/activate`.

- Install the dependencies with `pip install -r requirements.txt`.

- After the dependencies have installed, run the following commands :

  ```
   python manage.py makemigrations

   python manage.py migrate
  ```
- Start the developement server with

  ```
   python manage.py runserver
  ```
  
# Initial data for testing :
 
- Populate the database with initial test data by running the following command :
  ```
   python manage.py loaddata lucky_draw_api/fixtures/data.json
  ```
- The provided initial data has 7 users.

  | username      | password      |
  |:-------------:|:-------------:| 
  | admin         | admin         |
  | Kartik        | akashaviator  |
  | Satyam        | akashaviator  |
  | Shobhit       | akashaviator  |
  | Saurabh       | akashaviator  |
  | Shashwat      | akashaviator  |
  | Prateek       | akashaviator  |

- The test data includes 10 lucky draw raffles scheduled till April 7.
- **Note** - The raffles have been created by making the following assumptions -
  1. Raffles are held everyday from 8:00 AM till 8:00 PM.
  2. A winner can be declared by the admin only.
  3. A user should have an unused ticket to participate in a raffle.
  4. A user cannot participate in a raffle more than once.

# API Endpoints :

The API uses HTTP Basic Authentication , signed against a user's username and password, to authenticate api requests.

- `GET  http://127.0.0.1:8000/api/raffles`

  Returns the ongoing or upcoming raffle.
  

  **Example response** -
  ```json
  {
    "id": 7,
    "name": "Raffle 7",
    "prize": "Mobile",
    "opening_datetime": "04/04/2021, 08:00:00",
    "closing_datetime": "04/04/2021, 20:00:00"
  }
  ```

- `GET  http://127.0.0.1:8000/api/ticket`

  Creates a new ticket for the requesting user and returns its ticket id.

  **Example response** -
  ```json
    {
      "result": "successful",
      "ticket_id": 25
    }
  ```
- `GET  http://127.0.0.1:8000/api/user/tickets`

  Returns the unused tickets of the requesting user.
  
  **Example response** -
  ```json
    [
        {
            "id": 25,
            "used": false
        }
    ]
  ```
- `POST  http://127.0.0.1:8000/api/raffles`

  Participate in an ongoing raffle by providing a ticket id of an unused ticket.
  
  **Data params** -
  
    `ticket_id`
    
  *Example* - `{"ticket_id": 25}`
  
  **Example response** -
  ```json
    {
        "result": "Successful",
        "msg": "You have participated in the ongoing Lucky Draw raffle."
    }
  ```
- `GET  http://127.0.0.1:8000/api/raffles/winner`

  The Admin can make a request to this endpoint to declare a winner for the most recently concluded raffle.
  
  **Example response** -
  ```json
    {
        "result": "successful",
        "msg": "Winner for the previous raffle has been declared.",
        "username": "Prateek",
        "ticket_id": 20
    }
  ```
- `GET  http://127.0.0.1:8000/api/winners`

  Returns data about past raffles and their winners.
  
  **Example response** -
  ```json
    [
        {
            "raffle_name": "Raffle 7",
            "prize": "Mobile",
            "opening_datetime": "04/04/2021, 02:30:00",
            "closing_datetime": "04/04/2021, 14:30:00",
            "winner": "Prateek"
        },
        {
            "raffle_name": "Raffle 8",
            "prize": "Laptop",
            "opening_datetime": "03/04/2021, 18:48:21",
            "closing_datetime": "03/04/2021, 19:20:32",
            "winner": "Winner wasn't declared."
        }
    ]
  ```
# Code :

### Models:

The projects used two models located at [lucky_draw_api/models.py](https://github.com/akashaviator/LuckyDrawRaffle/blob/main/lucky_draw_api/models.py).

#### 1. LuckyDrawRaffle -
- Represents a lucky draw raffle.

#### 2. RaffleTicket -

- Represents a raffle ticket.

### URLs :

The `core/urls.py` file routes the api urls to [lucky_draw_api.urls](https://github.com/akashaviator/LuckyDrawRaffle/blob/main/lucky_draw_api/urls.py) which contains the API urls and routes them to API views.
```python
 path('api/', include('lucky_draw_api.urls')),
```

### Views :

The following API views are located in [lucky_draw_api/views.py](https://github.com/akashaviator/LuckyDrawRaffle/blob/main/lucky_draw_api/views.py) and serve the requests given alongside and described above under **API Endpoints**-

1. `GetTicketView`       -  `GET  /api/ticket`
2. `GetOwnTickets`       -  `GET  /api/user/tickets`
3. `LuckyDrawView`       -  `GET  /api/raffles` ,  `POST /api/raffles`
4. `AnnounceWinnerView`  -  `GET  /api/raffles/winner`
5. `ListWinnersView`     -  `GET  /api/winners`
