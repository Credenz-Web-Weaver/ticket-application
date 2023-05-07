# Ticket Show Application

## Setup and Local Environment Run

- Clone the project
- Run `cd ticket_application`
- Run `virtualenv venv`
- Run `venv/Scripts/Activate`
- Run `pip install -r "requirements.txt"`
- Run `python main.py`  

## Description of various files and folders
- `ticket_application` contains following directories
- `instance` has the sqlite DB. 
- `application` is where our application code is
- `static` - default `static` files folder. It serves at '/static' path.
- `templates` - Default flask templates folder
- `main.py` is the entry-point of the project.
- `requirements.txt` contains required python libraries.

##  Current features of this application
- A user can book tickets for shows.
- Admin can add/remove shows/venues.
- Aurhorization functionality

## Improvements that can be made
- Improved User Interface.
- Better management of Admin Dashboard
- Dynamic pricing for tickets
- Improvements in business logic
- Scheduled jobs to notify users about new shows/venues or send reminder messages
- Anymore innovative suggestion is also accepted.
