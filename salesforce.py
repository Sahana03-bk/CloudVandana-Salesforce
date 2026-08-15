import requests


API_VERSION = "v66.0"


def salesforce_headers(access_token):
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }


def get_records(
    access_token,
    instance_url,
    object_name,
    fields,
    limit=20,
    offset=0,
):
    headers = salesforce_headers(access_token)

    url = (
        f"{instance_url}/services/data/"
        f"{API_VERSION}/query"
    )

    # 1. Get the actual total number of records
    count_query = f"SELECT COUNT() FROM {object_name}"

    count_response = requests.get(
        url,
        headers=headers,
        params={"q": count_query},
    )

    if count_response.status_code != 200:
        raise Exception(
            f"Salesforce count API error: {count_response.text}"
        )

    total_size = count_response.json()["totalSize"]

    # 2. Get only 20 records for the current page
    field_list = ", ".join(fields)

    query = (
        f"SELECT {field_list} "
        f"FROM {object_name} "
        f"LIMIT {limit} "
        f"OFFSET {offset}"
    )

    response = requests.get(
        url,
        headers=headers,
        params={"q": query},
    )

    if response.status_code != 200:
        raise Exception(
            f"Salesforce API error: {response.text}"
        )

    result = response.json()

    # Use the real total count
    result["totalSize"] = total_size

    return result

def create_record(
    access_token,
    instance_url,
    object_name,
    record_data,
):
    url = (
        f"{instance_url}/services/data/"
        f"{API_VERSION}/sobjects/"
        f"{object_name}/"
    )

    response = requests.post(
        url,
        headers=salesforce_headers(access_token),
        json=record_data,
    )

    if response.status_code not in (200, 201):
        raise Exception(
            f"Salesforce API error: {response.text}"
        )

    return response.json()


def update_record(
    access_token,
    instance_url,
    object_name,
    record_id,
    record_data,
):
    url = (
        f"{instance_url}/services/data/"
        f"{API_VERSION}/sobjects/"
        f"{object_name}/"
        f"{record_id}"
    )

    response = requests.patch(
        url,
        headers=salesforce_headers(access_token),
        json=record_data,
    )

    if response.status_code not in (200, 204):
        raise Exception(
            f"Salesforce API error: {response.text}"
        )

    return {
        "success": True,
        "message": f"{object_name} updated successfully",
    }


def delete_record(
    access_token,
    instance_url,
    object_name,
    record_id,
):
    url = (
        f"{instance_url}/services/data/"
        f"{API_VERSION}/sobjects/"
        f"{object_name}/"
        f"{record_id}"
    )

    response = requests.delete(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    if response.status_code not in (200, 204):
        raise Exception(
            f"Salesforce API error: {response.text}"
        )

    return {
        "success": True,
        "message": f"{object_name} deleted successfully",
    }