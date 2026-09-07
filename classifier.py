import joblib

# Load trained AI model
model = joblib.load("models/ticket_classifier.pkl")


def classify_ticket(ticket):
    """
    Predict the category of a support ticket.
    """
    category = model.predict([ticket])[0]

    # Get confidence score
    probabilities = model.predict_proba([ticket])[0]
    confidence = max(probabilities) * 100

    return category, round(confidence, 2)


def predict_severity(ticket):
    """
    Predict severity using keyword-based rules.
    """
    text = ticket.lower()

    critical_words = [
        "server down",
        "entire company",
        "production down",
        "security breach"
    ]

    high_words = [
        "urgent",
        "cannot work",
        "business stopped",
        "client meeting",
        "vpn not working"
    ]

    medium_words = [
        "slow",
        "error",
        "problem",
        "issue"
    ]

    for word in critical_words:
        if word in text:
            return "Critical"

    for word in high_words:
        if word in text:
            return "High"

    for word in medium_words:
        if word in text:
            return "Medium"

    return "Low"


def calculate_priority(severity, business_impact):
    """
    Calculate ticket priority.
    """

    if severity == "Critical" and business_impact == "High":
        return "P1"

    elif severity == "High" and business_impact == "High":
        return "P1"

    elif severity == "High":
        return "P2"

    elif severity == "Medium":
        return "P3"

    else:
        return "P4"


def process_ticket(ticket, business_impact="High"):
    """
    Complete Milestone 1 processing.
    """

    # AI classification
    category, confidence = classify_ticket(ticket)

    # Severity prediction
    severity = predict_severity(ticket)

    # Priority calculation
    priority = calculate_priority(
        severity,
        business_impact
    )

    return category, severity, priority, confidence


# Test the system
if __name__ == "__main__":

    ticket = """
    URGENT: VPN is not connecting.
    I cannot work and I have an important client meeting.
    """

    category, severity, priority, confidence = process_ticket(ticket)

    print("Ticket:", ticket)
    print("Category:", category)
    print("Severity:", severity)
    print("Priority:", priority)
    print("Confidence:", confidence, "%")