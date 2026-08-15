from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from oauth import (
    get_salesforce_authorization_url,
    exchange_code_for_token,
)

from salesforce import (
    get_records,
    create_record,
    update_record,
    delete_record,
)


app = FastAPI(
    title="CloudVandana Salesforce CRUD App"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)

# Temporary storage for development/testing
salesforce_session = {}


# Fields we will display for each Salesforce object
OBJECT_FIELDS = {
    "Account": [
        "Id",
        "Name",
        "Type",
        "Industry",
        "Phone",
    ],
    "Contact": [
        "Id",
        "FirstName",
        "LastName",
        "Email",
        "Phone",
    ],
    "Lead": [
        "Id",
        "FirstName",
        "LastName",
        "Company",
        "Email",
    ],
    "Opportunity": [
        "Id",
        "Name",
        "StageName",
        "CloseDate",
        "Amount",
    ],
    "Case": [
    "Id",
    "CaseNumber",
    "Subject",
    "Status",
    "Priority",
    "Origin",
],
}


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/health")
def health():
    return {
        "status": "OK"
    }


@app.get("/auth/login")
def salesforce_login():

    authorization_url = (
        get_salesforce_authorization_url()
    )

    return RedirectResponse(
        url=authorization_url
    )


@app.get("/auth/callback")
def salesforce_callback(
    code: str,
    state: str,
):

    token_data = exchange_code_for_token(
        code,
        state
    )

    salesforce_session["access_token"] = (
        token_data["access_token"]
    )

    salesforce_session["instance_url"] = (
        token_data["instance_url"]
    )

    return RedirectResponse(url="/")


# --------------------------------------------------
# GET RECORDS
# --------------------------------------------------

@app.get("/records/{object_name}")
def read_records(
    object_name: str,
    offset: int = 0,
):
    if "access_token" not in salesforce_session:
        raise HTTPException(
            status_code=401,
            detail="Please login with Salesforce first."
        )

    if object_name not in OBJECT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail="Invalid Salesforce object."
        )

    if offset < 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid offset."
        )

    try:
        result = get_records(
            salesforce_session["access_token"],
            salesforce_session["instance_url"],
            object_name,
            OBJECT_FIELDS[object_name],
            limit=20,
            offset=offset,
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# CREATE RECORD
# --------------------------------------------------

@app.post("/records/{object_name}")
def create_new_record(
    object_name: str,
    record_data: dict,
):

    if "access_token" not in salesforce_session:
        raise HTTPException(
            status_code=401,
            detail="Please login with Salesforce first."
        )

    if object_name not in OBJECT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail="Invalid Salesforce object."
        )

    try:

        result = create_record(
            salesforce_session["access_token"],
            salesforce_session["instance_url"],
            object_name,
            record_data,
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# UPDATE RECORD
# --------------------------------------------------

@app.patch("/records/{object_name}/{record_id}")
def update_existing_record(
    object_name: str,
    record_id: str,
    record_data: dict,
):

    if "access_token" not in salesforce_session:
        raise HTTPException(
            status_code=401,
            detail="Please login with Salesforce first."
        )

    if object_name not in OBJECT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail="Invalid Salesforce object."
        )

    try:

        result = update_record(
            salesforce_session["access_token"],
            salesforce_session["instance_url"],
            object_name,
            record_id,
            record_data,
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# DELETE RECORD
# --------------------------------------------------

@app.delete("/records/{object_name}/{record_id}")
def delete_existing_record(
    object_name: str,
    record_id: str,
):

    if "access_token" not in salesforce_session:
        raise HTTPException(
            status_code=401,
            detail="Please login with Salesforce first."
        )

    if object_name not in OBJECT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail="Invalid Salesforce object."
        )

    try:

        result = delete_record(
            salesforce_session["access_token"],
            salesforce_session["instance_url"],
            object_name,
            record_id,
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@app.get("/api/auth/status")
def auth_status():
    return {
        "logged_in": "access_token" in salesforce_session
    }        