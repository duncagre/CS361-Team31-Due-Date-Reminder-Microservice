import json
import urllib.request
import urllib.error
from datetime import datetime, date, timedelta

BASE_URL = "http://127.0.0.1:5001"

#   -------------------------
#   Request helper
#   -------------------------

def post_json(route, payload):
    """
    Sends a POST request with JSON data.
    """
    url = BASE_URL + route
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode("utf-8")
            return response.status, json.loads(response_data)
    except urllib.error.HTTPError as error:
        response_data = error.read().decode("utf-8")
        return error.code, json.loads(response_data)


#   -------------------------
#   Test functions
#   -------------------------

def test_set_due_date_success():
    """
    Tests setting a valid due date.
    """
    status, response = post_json("/set-due-date", {
        "task_id": "1",
        "due_date": "2026-03-20"
    })

    print("\nTest: set valid due date")
    print("Status:", status)
    print("Response:", response)


def test_set_due_date_invalid_format():
    """
    Tests setting an invalid due date format.
    """
    status, response = post_json("/set-due-date", {
        "task_id": "2",
        "due_date": "03-20-2026"
    })

    print("\nTest: set invalid due date format")
    print("Status:", status)
    print("Response:", response)


def test_due_soon():
    """
    Tests finding tasks due soon.
    """
    today = date.today()
    date_1 = str(today + timedelta(days=2))
    date_2 = str(today + timedelta(days=10))

    status, response = post_json("/due-soon", {
        "days": 7,
        "tasks": [
            {"task_id": "1", "title": "Task A", "due_date": date_1},
            {"task_id": "2", "title": "Task B", "due_date": date_2},
            {"task_id": "3", "title": "Task C", "due_date": ""}
        ]
    })

    print("\nTest: due soon")
    print("Status:", status)
    print("Response:", response)


def test_overdue():
    """
    Tests finding overdue tasks.
    """
    today = date.today()
    date_1 = str(today - timedelta(days=3))
    date_2 = str(today + timedelta(days=5))

    status, response = post_json("/overdue", {
        "tasks": [
            {"task_id": "1", "title": "Task A", "due_date": date_1},
            {"task_id": "2", "title": "Task B", "due_date": date_2},
            {"task_id": "3", "title": "Task C", "due_date": ""}
        ]
    })

    print("\nTest: overdue")
    print("Status:", status)
    print("Response:", response)


#   -------------------------
#   Run tests
#   -------------------------

if __name__ == "__main__":
    test_set_due_date_success()
    test_set_due_date_invalid_format()
    test_due_soon()
    test_overdue()