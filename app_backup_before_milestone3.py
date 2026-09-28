from flask import Flask, render_template, request, redirect, url_for, make_response
from functools import wraps
import jwt
from datetime import datetime, timedelta

from classifier import process_ticket

from database import (
    create_database,
    save_ticket,
    get_tickets,
    get_ticket,
    update_ticket_status
)

from rag_pipeline import run_rag_pipeline
from retriever import KnowledgeRetriever
from knowledge_base import knowledge_base


app = Flask(__name__)


# =========================================================
# DATABASE
# =========================================================

create_database()


# =========================================================
# JWT SECRET KEY
# =========================================================

SECRET_KEY = "supportpilot-secret-key-2026-super-secret"


# =========================================================
# CREATE JWT TOKEN
# =========================================================

def create_token(username):

    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    return token


# =========================================================
# JWT PROTECTION
# =========================================================

def token_required(view_function):

    @wraps(view_function)
    def decorated_function(*args, **kwargs):

        token = request.cookies.get("access_token")

        # No token
        if not token:
            return redirect(url_for("login"))

        try:

            jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

        except jwt.ExpiredSignatureError:

            response = make_response(
                redirect(url_for("login"))
            )

            response.delete_cookie("access_token")

            return response

        except jwt.InvalidTokenError:

            response = make_response(
                redirect(url_for("login"))
            )

            response.delete_cookie("access_token")

            return response

        return view_function(*args, **kwargs)

    return decorated_function


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        # College demo:
        # Any non-empty username and password are accepted

        if username and password:

            token = create_token(username)

            response = make_response(
                redirect(url_for("dashboard"))
            )

            response.set_cookie(
                "access_token",
                token,
                httponly=True,
                max_age=7200
            )

            return response

    return render_template("login.html")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    response = make_response(
        redirect(url_for("login"))
    )

    response.delete_cookie("access_token")

    return response


# =========================================================
# HOME / NEW TICKET
# =========================================================

@app.route("/", methods=["GET", "POST"])
@token_required
def home():

    result = None

    if request.method == "POST":

        data = {

            "employee_name": request.form.get(
                "employee_name",
                ""
            ),

            "email": request.form.get(
                "email",
                ""
            ),

            "title": request.form.get(
                "title",
                ""
            ),

            "description": request.form.get(
                "description",
                ""
            ),

            "department": request.form.get(
                "department",
                ""
            )
        }

        # =================================================
        # ML CLASSIFICATION
        # =================================================

        category, severity, priority, confidence = process_ticket(
            data["description"],
            "High"
        )

        data["category"] = category
        data["severity"] = severity
        data["priority"] = priority
        data["confidence"] = confidence
        data["status"] = "Open"


        # =================================================
        # RAG PIPELINE
        # =================================================

        ticket = {

            "id": "TEMP",

            "title": data["title"],

            "description": data["description"],

            "category": data["category"],

            "severity": data["severity"],

            "priority": data["priority"],

            "confidence": data["confidence"]

        }

        rag_result = run_rag_pipeline(ticket)


        data["resolution"] = rag_result.get(
            "resolution",
            "No resolution generated."
        )


        # =================================================
        # SAVE TICKET
        # =================================================

        save_ticket(data)

        result = data


    return render_template(
        "index.html",
        result=result
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@token_required
def dashboard():

    tickets = get_tickets()


    # =================================================
    # SEARCH / FILTER
    # =================================================

    search = request.args.get(
        "search",
        ""
    ).strip().lower()

    status_filter = request.args.get(
        "status",
        ""
    )

    priority_filter = request.args.get(
        "priority",
        ""
    )

    category_filter = request.args.get(
        "category",
        ""
    )


    filtered_tickets = []


    for ticket in tickets:

        text = (
            str(ticket["title"]) +
            " " +
            str(ticket["description"]) +
            " " +
            str(ticket["employee_name"])
        ).lower()


        if search and search not in text:
            continue


        if (
            status_filter and
            ticket["status"] != status_filter
        ):
            continue


        if (
            priority_filter and
            ticket["priority"] != priority_filter
        ):
            continue


        if (
            category_filter and
            ticket["category"] != category_filter
        ):
            continue


        filtered_tickets.append(ticket)


    # =================================================
    # STATISTICS
    # =================================================

    total = len(tickets)


    open_tickets = sum(
        1
        for ticket in tickets
        if ticket["status"] == "Open"
    )


    high_priority = sum(
        1
        for ticket in tickets
        if ticket["priority"] == "P1"
    )


    resolved_tickets = sum(
        1
        for ticket in tickets
        if ticket["status"] == "Resolved"
    )


    # =================================================
    # CHART DATA
    # =================================================

    status_data = {

        "Open": 0,

        "In Progress": 0,

        "Resolved": 0

    }


    priority_data = {

        "P1": 0,

        "P2": 0,

        "P3": 0,

        "P4": 0

    }


    category_data = {}


    for ticket in tickets:

        # Status

        status = ticket["status"]

        if status not in status_data:

            status_data[status] = 0

        status_data[status] += 1


        # Priority

        priority = ticket["priority"]

        if priority not in priority_data:

            priority_data[priority] = 0

        priority_data[priority] += 1


        # Category

        category = ticket["category"]

        if category not in category_data:

            category_data[category] = 0

        category_data[category] += 1


    # =================================================
    # KNOWLEDGE RETRIEVER
    # =================================================

    retriever = KnowledgeRetriever(
        knowledge_base
    )


    ticket_data = []


    for ticket in filtered_tickets:

        query = (
            str(ticket["title"]) +
            " " +
            str(ticket["description"])
        )


        retrieved_docs = retriever.search(
            query,
            top_k=3
        )


        ticket_data.append({

            "ticket": ticket,

            "retrieved_docs": retrieved_docs

        })


    # =================================================
    # RENDER DASHBOARD
    # =================================================

    return render_template(

        "dashboard.html",

        ticket_data=ticket_data,

        total=total,

        open_tickets=open_tickets,

        high_priority=high_priority,

        resolved_tickets=resolved_tickets,

        status_data=status_data,

        priority_data=priority_data,

        category_data=category_data,

        search=search,

        status_filter=status_filter,

        priority_filter=priority_filter,

        category_filter=category_filter

    )


# =========================================================
# TICKET DETAILS
# =========================================================

@app.route("/ticket/<int:ticket_id>")
@token_required
def ticket_details(ticket_id):

    ticket = get_ticket(ticket_id)


    if ticket is None:

        return "Ticket not found", 404


    # =================================================
    # RETRIEVE KNOWLEDGE BASE
    # =================================================

    retriever = KnowledgeRetriever(
        knowledge_base
    )


    query = (

        str(ticket["title"]) +

        " " +

        str(ticket["description"])

    )


    retrieved_docs = retriever.search(

        query,

        top_k=3

    )


    # =================================================
    # RENDER TICKET DETAILS
    # =================================================

    return render_template(

        "ticket_details.html",

        ticket=ticket,

        retrieved_docs=retrieved_docs

    )


# =========================================================
# UPDATE TICKET STATUS
# =========================================================

@app.route(
    "/ticket/<int:ticket_id>/status",
    methods=["POST"]
)
@token_required
def update_status(ticket_id):

    new_status = request.form.get(
        "status",
        ""
    )


    allowed_statuses = [

        "Open",

        "In Progress",

        "Resolved"

    ]


    if new_status not in allowed_statuses:

        return "Invalid status", 400


    # Check ticket exists

    ticket = get_ticket(ticket_id)


    if ticket is None:

        return "Ticket not found", 404


    update_ticket_status(

        ticket_id,

        new_status

    )


    return redirect(

        url_for(

            "ticket_details",

            ticket_id=ticket_id

        )

    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )