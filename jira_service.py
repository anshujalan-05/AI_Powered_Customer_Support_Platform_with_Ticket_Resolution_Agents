
import os
import requests
from requests.auth import HTTPBasicAuth


def create_jira_ticket(ticket):
    jira_url = os.getenv("JIRA_URL")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    jira_project_key = os.getenv("JIRA_PROJECT_KEY")

    if not all([
        jira_url,
        jira_email,
        jira_api_token,
        jira_project_key
    ]):
        return {
            "success": False,
            "message": "Jira configuration is missing.",
            "ticket_id": None
        }

    api_url = f"{jira_url.rstrip('/')}/rest/api/3/issue"

    description = (
        f"Employee: {ticket.get('employee_name', 'N/A')}\n"
        f"Email: {ticket.get('email', 'N/A')}\n"
        f"Department: {ticket.get('department', 'N/A')}\n"
        f"Category: {ticket.get('category', 'N/A')}\n"
        f"Description: {ticket.get('description', 'N/A')}\n"
        f"AI Resolution: {ticket.get('resolution', 'N/A')}"
    )

    payload = {
        "fields": {
            "project": {
                "key": jira_project_key
            },
            "summary": ticket.get(
                "title",
                "SupportPilot Support Ticket"
            ),
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Task"
            }
        }
    }

    try:
        response = requests.post(
            api_url,
            json=payload,
            auth=HTTPBasicAuth(
                jira_email,
                jira_api_token
            ),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            timeout=20
        )

        if response.status_code == 201:
            response_data = response.json()

            return {
                "success": True,
                "message": "Jira ticket created successfully.",
                "ticket_id": response_data.get("key")
            }

        return {
            "success": False,
            "message": f"Jira API error: {response.status_code}",
            "ticket_id": None
        }

    except requests.exceptions.RequestException as error:
        return {
            "success": False,
            "message": f"Jira connection failed: {error}",
            "ticket_id": None
        }