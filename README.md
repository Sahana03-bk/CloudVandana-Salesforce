# CloudVandana Salesforce CRUD Application

A full-stack web application built using **FastAPI** and the **Salesforce REST API** to perform CRUD operations on Salesforce records.

The application uses **Salesforce OAuth 2.0 authentication** and provides a simple web interface for managing Salesforce records.

## Live Application

**Deployed Application:**

https://cloudvandana-salesforce-production.up.railway.app/

## GitHub Repository

https://github.com/Sahana03-bk/CloudVandana-Salesforce
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

Existing Salesforce records can be deleted through the application.

Salesforce may prevent deletion of records that have dependent or related records. In such cases, the application displays the Salesforce API error instead of treating it as an application failure.

For example, Salesforce may prevent deletion of an Account or Contact when related Cases or other dependent records exist.

## Pagination

The application uses pagination to avoid loading all Salesforce records at once.

Records are retrieved in batches using:

LIMIT 20
OFFSET <offset>

The application also retrieves the total number of records using a count query.

Example:

20 of 21 records

When the user reaches the bottom of the table, the next batch of records is loaded.
### API Endpoints
## Salesforce Login
```GET /auth/login```

Starts the Salesforce OAuth authentication process.

## OAuth Callback
```GET /auth/callback```

Handles the Salesforce OAuth callback and stores the access token.

## Get Records
```GET /records/{object_name}```
Example:
```GET /records/Account?offset=0```
## Create Record
```POST /records/{object_name}```
## Update Record
```PUT /records/{object_name}/{record_id}```
## Delete Record
```DELETE /records/{object_name}/{record_id}```
## API Documentation
FastAPI automatically provides Swagger documentation at:
```/docs```
When running locally:
http://127.0.0.1:8000/docs

## Environment Variables

Sensitive Salesforce credentials should be stored in a .env file and should never be committed to GitHub.

Example:
```
SALESFORCE_CLIENT_ID=your_client_id
SALESFORCE_CLIENT_SECRET=your_client_secret
SALESFORCE_REDIRECT_URI=http://127.0.0.1:8000/auth/callback
SALESFORCE_LOGIN_URL=https://login.salesforce.com
```
For the deployed application, the callback URL is configured using the Railway environment variables.
```https://cloudvandana-salesforce-production.up.railway.app/auth/callback```
### Installation
## 1. Clone the repository
```git clone https://github.com/Sahana03-bk/CloudVandana-Salesforce.git```
## 2. Navigate to the project
```cd CloudVandana-Salesforce```
## 3. Create a virtual environment
Windows:
```python -m venv venv```
## 4. Activate the virtual environment
Windows PowerShell:
```venv\Scripts\Activate.ps1```
## 5. Install dependencies
```pip install -r requirements.txt```
## 6. Configure environment variables
Create a .env file:
```
SALESFORCE_CLIENT_ID=your_client_id
SALESFORCE_CLIENT_SECRET=your_client_secret
SALESFORCE_REDIRECT_URI=http://127.0.0.1:8000/auth/callback
SALESFORCE_LOGIN_URL=https://login.salesforce.com
```
## 7. Start the application
```uvicorn main:app --reload```
The application will run at:
http://127.0.0.1:8000

## Testing

The API can be tested using FastAPI Swagger UI:

```http://127.0.0.1:8000/docs```

The following operations were tested:

Salesforce authentication
Account creation
Contact creation
Lead creation
Opportunity creation
Case creation
Record retrieval
Record update
Record deletion
Pagination
Salesforce deletion restrictions
Error handling

## Error Handling

The application handles:

Missing Salesforce authentication
Invalid Salesforce object names
Invalid pagination offsets
Salesforce API errors
Salesforce record deletion restrictions
Authentication failures

Salesforce-specific errors are returned to the frontend so that users receive meaningful notifications.

## Security

Sensitive credentials are not stored in source code.

The following files and directories are excluded from Git:
```
.env
venv/
__pycache__/
*.pyc
```
Salesforce access tokens are handled by the application session and are not intended to be committed to the repository.
# Deployment
The application is deployed using Railway.

Live application:

```https://cloudvandana-salesforce-production.up.railway.app/```

The deployed application uses Salesforce OAuth authentication and communicates with Salesforce through the Salesforce REST API.
# Author
Sahana B K

