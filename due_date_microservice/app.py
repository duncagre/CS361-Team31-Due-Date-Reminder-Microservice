from flask import Flask, request, jsonify
from datetime import datetime, dat, timedelta, date
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "due_dates.json"))

#   -------------------------
#   File load/save
#   -------------------------

def load_data():
    """
    Loads saved due date data from a JSON file.
    If the file does not exist or is invalid, returns empty data.
    """
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r"), encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return {}

        return data
    except (OSError, json.JSONDecodeError):
        return {}



def save_data(data):
    """
    Saves the current due date data to a JSON file.
    """
    os.makedirs(os.path.dirname(DATAFILE), exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


#   -------------------------
#   General helper functions
#   -------------------------

def is_blank(text):
    """
    Checks whether the given text is blank.
    """
    return str(text).strip() == ""


def is_valid_date_string(date_text):
    """
    Checks whether the given date string is valid.
    Expected format: YYYY-MM-DD
    """
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


#   -------------------------
#   Due date logic
#   -------------------------

def set_due_date_for_task(data, task_id, due_date):
    """
    Saves or updates the due date for a task.
    """
    data[task_id] = due_date
    save_data(data)


def get_tasks_due_soon(task_list, days):
    """
    Returns tasks due within the next given number of days.
    """
    results = []
    today = date.today()
    end_date = today + timedelta(days=days)

    for task in task_list:
        if "due_date" in task:
            due_date_text = task["due_date"]

            if is_valid_date_string(due_date_text):
                due_date_obj = datetime.strptime(due_date_text, "%Y-%m-%d").date()

                if due_date_obj < today:
                    results.append(task)

    return results


def get_overdue_tasks(task_list):
    """
    Returns tasks that are overdue.
    """
    for task in task_list:
        if "due_date" in task:
            due_date_text = task["due_date"]

            if is_valid_date_string(due_date_text):
                due_date_obj = datetime.strptime(due_date_text, "%Y-%m-%d").date()

                if due_date_obj < today:
                    results.append(task)

    return results


#   -------------------------
#   Routes
#   -------------------------

@app.route("/")
def home():
    """
    Confirms the microservice is running.
    """
    return jsonify({"message": "Due Date and Reminder Microservice running."})


@app.route("/set-due-date", methods=["POST"])
def set_due_date():
    """
    Saves or updates the due date for a task.
    """
    data = load_data()
    body = request.get_json()

    if body is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    task_id = str(body.get("task_id", "")).strip()
    due_date = str(body.get("due_date", "")).strip()

    if is_blank(task_id):
        return jsonify({"error": "task_id is required."}), 400

    if is_blank(due_date):
        return jsonify({"error": "due_date is required."}), 400

    if not is_valid_date_string(due_date):
        return jsonify({"error": "due_date must be in YYYY-MM-DD format."}), 400

    set_due_date_for_task(data, task_id, due_date)

    return jsonify({
        "status": "success",
        "task_id": task_id,
        "due_date": due_date,
    }), 200


@app.route("/due-soon", methods=["POST"])
def due_soon():
    """
    Returns tasks due within the next given number of days.
    """
    body = request.get_json()

    if body is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    tasks = body.get("tasks", [])
    days = body.get("days", 0)

    if not isinstance(tasks, list):
        return jsonify({"error": "tasks must be a list."}), 400

    if not isinstance(days, int):
        return jsonify({"error": "days must be an integer."}), 400

    if days < 0:
        return jsonify({"error": "days cannot be negative."}), 400

    due_soon_tasks = get_tasks_due_soon(tasks, days)

    return jsonify({
        "status": "success",
        "tasks": due_soon_tasks,
    }), 200


@app.route("/overdue", methods=["POST"])
def overdue():
    """
    Returns tasks that are overdue.
    """
    body = request.get_json()

    if body is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    tasks = body.get("tasks", [])

    if not isinstance(tasks, list):
        return jsonify({"error": "tasks must be a list."}), 400

    overdue_tasks = get_overdue_tasks(tasks)

    return jsonify({
        "status": "success",
        "tasks": overdue_tasks,
    }), 200


#   -------------------------
#   Run microservice
#   -------------------------

if __name__ == "__main__":
    print("Starting Due Date and Reminder Microservice...")
    app.run(port=5001)