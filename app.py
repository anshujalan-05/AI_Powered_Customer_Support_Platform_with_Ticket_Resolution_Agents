from flask import Flask, render_template, request
from classifier import process_ticket
from database import create_database, save_ticket, get_tickets

app = Flask(__name__)

create_database()


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        data = {
            "employee_name": request.form["employee_name"],
            "email": request.form["email"],
            "title": request.form["title"],
            "description": request.form["description"],
            "department": request.form["department"]
        }

        category, severity, priority, confidence = process_ticket(
            data["description"],
            "High"
        )

        data["category"] = category
        data["severity"] = severity
        data["priority"] = priority
        data["confidence"] = confidence
        data["status"] = "Open"

        save_ticket(data)

        result = data

    return render_template("index.html", result=result)


@app.route("/dashboard")
def dashboard():

    tickets = get_tickets()

    total = len(tickets)
    open_tickets = sum(t["status"] == "Open" for t in tickets)
    high_priority = sum(t["priority"] == "P1" for t in tickets)

    return render_template(
        "dashboard.html",
        tickets=tickets,
        total=total,
        open_tickets=open_tickets,
        high_priority=high_priority
    )


if __name__ == "__main__":
    app.run(debug=True)