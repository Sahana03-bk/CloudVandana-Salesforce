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

```Application
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
```
# CRUD Operations
## Create

The application allows users to create records for:

Account
Contact
Lead
Opportunity
Case
Read

Records are retrieved from Salesforce using SOQL queries through the Salesforce REST API.

## Update

Existing Salesforce records can be edited and updated through the application.

## Delete

Records can be deleted through the application.

Salesforce may prevent deletion of records that have dependent or related records. In such cases, the application displays the Salesforce error instead of treating it as an application crash.

For example, an Account or Contact associated with Cases may not be deleted by Salesforce.

## Pagination

The application uses pagination to avoid loading all Salesforce records at once.

Records are retrieved in batches using:

LIMIT 20
OFFSET <offset>

The application also retrieves the total number of records using a count query.

Example:

20 of 21 records

When the user reaches the bottom of the table, the next batch of records is loaded.
API Endpoints
Salesforce Login
GET /auth/login

Starts the Salesforce OAuth authentication process.

OAuth Callback
GET /auth/callback

Handles the Salesforce OAuth callback and stores the access token.

Get Records
GET /records/{object_name}

Example:

GET /records/Account?offset=0
Create Record
POST /records/{object_name}
Update Record
PUT /records/{object_name}/{record_id}
Delete Record
DELETE /records/{object_name}/{record_id}
