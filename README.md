# CS361-Team31-Due-Date-Reminder-Microservice

Due Date and Reminder microservice for CS361 Team 31.  
Provides task due date management and reminder functionality via REST API using JSON.

---

## DESCRIPTION

This microservice allows a client to:

- Assign or update a due date for a task.
- Retrieve tasks that are due within a specified number of days.
- Retrieve tasks that are overdue.

Dates must follow the format `YYYY-MM-DD`.

The service communicates exclusively via HTTP POST requests using JSON.

---

## INSTALLATION

Install required packages:

```bash
pip install flask
```

Run the application:

```bash
python app.py
```

The service runs on:

```
http://127.0.0.1:5001
```

---

## HOW TO REQUEST DATA

All requests must:
- Use HTTP POST
- Include header: `Content-Type: application/json`
- Include a JSON body

### POST /set-due-date

Required JSON fields:
- `task_id` (string)
- `due_date` (string)

Example request:

```bash
curl -X POST http://127.0.0.1:5001/set-due-date \
-H "Content-Type: application/json" \
-d "{\"task_id\":\"task1\",\"due_date\":\"2026-03-20\"}"
```

---

### POST /due-soon

Required JSON fields:
- `tasks` (array of objects containing `task_id` and `due_date`)
- `days` (integer)

Example request:

```bash
curl -X POST http://127.0.0.1:5001/due-soon \
-H "Content-Type: application/json" \
-d "{\"tasks\":[{\"task_id\":\"task1\",\"due_date\":\"2026-03-20\"}],\"days\":7}"
```

---

### POST /overdue

Required JSON fields:
- `tasks` (array of objects containing `task_id` and `due_date`)

Example request:

```bash
curl -X POST http://127.0.0.1:5001/overdue \
-H "Content-Type: application/json" \
-d "{\"tasks\":[{\"task_id\":\"task1\",\"due_date\":\"2026-03-10\"}]}"
```

---

## HOW TO RECEIVE DATA

All responses are returned in JSON format.

### /set-due-date responses

Success (200 OK):

```json
{
  "status": "success",
  "task_id": "task1",
  "due_date": "2026-03-20"
}
```

Failure (400 Bad Request):

```json
{
  "status": "error",
  "message": "Invalid JSON"
}
```

```json
{
  "status": "error",
  "message": "Invalid date format"
}
```

---

### /due-soon responses

Success (200 OK):

```json
{
  "status": "success",
  "tasks": []
}
```

---

### /overdue responses

Success (200 OK):

```json
{
  "status": "success",
  "tasks": []
}
```

---

## TEST PROGRAM

To test using the provided test client:

1. Run the microservice:

```bash
python app.py
```

2. In a separate terminal, run:

```bash
python test_due_date.py
```

The test program sends POST requests to `/set-due-date`, `/due-soon`, and `/overdue` and prints the JSON responses returned by the microservice.