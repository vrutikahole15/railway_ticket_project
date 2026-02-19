# railway_ticket_project
# Railway-Ticket-Reservation-API
Table of Contents

1. Project Overview
2. Setup Instructions
  Prerequisites
  Installation Steps
3. Architecture
  MVT Pattern
  Component Interaction
4. Flowcharts
  User Registration and Authentication
  Ticket Booking Process
5. Sample Requests
  User Registration
  User Login
  View Available Tickets
  Book a Ticket
  Cancel a Ticket
1. Project Overview
The Railway Ticket Reservation API is designed to manage user registrations, authenticate users, and facilitate ticket booking and cancellation for railway services. It provides endpoints for:

User registration and authentication
Viewing available tickets
Booking tickets
Canceling booked tickets
2. Setup Instructions
2.1 Prerequisites
Before setting up the project, ensure you have the following installed:

Python 3.8+: The programming language used for development.
Django 3.2+: The web framework utilized.
pip: Python package installer.
Virtualenv: Tool to create isolated Python environments.
2.2 Installation Steps
Clone the Repository

git clone https://github.com/YuvrajShinde-02/railway-ticket-reservation-api.git
cd railway-ticket-reservation-api
Create and Activate a Virtual Environment
python -m venv env
# On Windows
env\Scripts\activate
# On macOS/Linux
source env/bin/activate
Install Dependencies
pip install -r requirements.txt

3. Architecture
3.1 MVT Pattern
The project follows Django's Model-View-Template (MVT) architecture:

Model: Defines the data structure. In this project, models represent Users, Tickets, and Bookings.
View: Contains the business logic and interacts with the model to carry data to the template.
Template: Renders the data for the user interface.
3.2 Component Interaction
[Client] <---> [URLs] <---> [Views] <---> [Models] <---> [Database]
Client: Makes HTTP requests to the API.
URLs: Routes the requests to the appropriate view.
Views: Processes the request, interacts with models, and returns a response.
Models: Represents the data and handles database interactions.
Database: Stores the data.
 +-----------------------+
          |   Client (Browser)    |
          +-----------------------+
                      |
                      ↓
      +-------------------------------+
      |       Django Server API      |
      +-------------------------------+
                      |
          +-------------------------+
          |       Database           |
          +-------------------------+
API EndpointsBook TicketPOST /api/v1/tickets/book
Request Body:
{
  "name": "John Doe",
  "age": 45,
  "gender": "male",
  "has_children": false
}
Cancel TicketPOST /api/v1/tickets/cancel/{ticketId}
View Booked TicketsGET /api/v1/tickets/booked
View Available TicketsGET /api/v1/tickets/available

Templates and RoutingAPI Root: /api/v1/tickets/
Book Ticket Page: /book
Cancel Ticket Page: /cancel/
View Booked Tickets: /booked
View Available Tickets: /available
After submitting forms, users are redirected to the API root.
