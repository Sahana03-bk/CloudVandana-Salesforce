# CloudVandana-Salesforce
# CloudVandana Salesforce CRUD Application

A full-stack web application built using **FastAPI** and **Salesforce REST API** to perform CRUD operations on Salesforce records.

The application authenticates users through Salesforce OAuth and provides a simple web interface for managing Salesforce records.

## Features

- Salesforce OAuth 2.0 authentication
- Salesforce REST API integration
- Create Salesforce records
- Read Salesforce records
- Update Salesforce records
- Delete Salesforce records
- Pagination / infinite scrolling
- Dynamic forms based on Salesforce objects
- Record count display
- Success and error notifications
- Salesforce error handling
- Responsive web interface

## Salesforce Objects

The application supports the following Salesforce objects:

- Account
- Contact
- Lead
- Opportunity
- Case

## Technologies Used

### Backend

- Python
- FastAPI
- Uvicorn
- Requests

### Frontend

- HTML5
- CSS3
- JavaScript

### Database / CRM

- Salesforce
- Salesforce REST API
- SOQL

### Authentication

- Salesforce OAuth 2.0

### Development Tools

- Git
- GitHub
- Visual Studio Code

## Project Structure

```text
CloudVandana-Salesforce/
│
├── main.py
├── oauth.py
├── salesforce.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    ├── app.js
    └── style.css
```

## Application Architecture

```User
  │
  ▼
Web Interface
  │
  ▼
FastAPI Backend
  │
  ├── OAuth Authentication
  │
  ├── CRUD APIs
  │
  └── Pagination
  │
  ▼
Salesforce REST API
  │
  ▼
Salesforce Objects
(Account / Contact / Lead / Opportunity / Case)
```
## Salesforce Authentication
Application
    │
    ▼
Salesforce Login
    │
    ▼
OAuth Authorization
    │
    ▼
Authorization Code
    │
    ▼
FastAPI Callback
    │
    ▼
Access Token
    │
    ▼
Salesforce REST API
