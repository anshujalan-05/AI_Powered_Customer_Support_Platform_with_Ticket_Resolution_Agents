import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os

data = {
    "ticket": [

        # NETWORK
        "WiFi is not working",
        "Internet connection is not working",
        "Network is disconnected",
        "Unable to connect to WiFi",
        "Internet connection is very slow",
        "My network is down",
        "Cannot access the internet",
        "WiFi connection keeps dropping",
        "Network connectivity problem",
        "Office internet is not working",
        "Unable to connect to office network",
        "Internet connection failed",

        # VPN
        "VPN is not connecting",
        "Unable to access company VPN",
        "VPN connection failed",
        "Company VPN is not working",
        "I cannot connect to VPN",
        "VPN stopped working",
        "Unable to login through VPN",
        "VPN connection keeps failing",
        "Remote VPN access is not working",
        "VPN access problem",
        "Company VPN connection failed",
        "I am unable to use the VPN",

        # PASSWORD
        "I forgot my password",
        "Please reset my password",
        "Password is not working",
        "I cannot login because I forgot my password",
        "Unable to login with my password",
        "Password reset required",
        "I need to change my password",
        "My password has expired",
        "Forgot password and cannot login",
        "Account password problem",
        "Login password is not working",
        "Please help me reset my password",

        # SOFTWARE
        "Install Microsoft Office",
        "Application installation required",
        "I need software installed",
        "Please install the required application",
        "Software installation problem",
        "I need a new application installed",
        "Please install Microsoft Office",
        "Application is missing from my laptop",
        "Need installation of company software",
        "Software installation required",
        "Please install the software",
        "I cannot install the application",

        # HARDWARE
        "Laptop keyboard is not working",
        "Monitor display is not working",
        "My laptop screen is broken",
        "Keyboard keys are not responding",
        "Laptop hardware problem",
        "Computer mouse is not working",
        "Monitor is not displaying anything",
        "Laptop keyboard stopped working",
        "My computer screen is not working",
        "Hardware failure on my laptop",
        "Laptop charger is not working",
        "My mouse is not responding",

        # SYSTEM
        "Computer system is not responding",
        "Windows is not starting",
        "System keeps crashing",
        "My computer is very slow",
        "System error occurred",
        "Windows is showing an error",
        "Computer freezes frequently",
        "Operating system is not working",
        "System troubleshooting required",
        "My computer keeps restarting",
        "Windows system problem",
        "The system is stuck"
    ],

    "category": [

        # NETWORK
        "Network","Network","Network","Network",
        "Network","Network","Network","Network",
        "Network","Network","Network","Network",

        # VPN
        "VPN","VPN","VPN","VPN",
        "VPN","VPN","VPN","VPN",
        "VPN","VPN","VPN","VPN",

        # PASSWORD
        "Password","Password","Password","Password",
        "Password","Password","Password","Password",
        "Password","Password","Password","Password",

        # SOFTWARE
        "Software","Software","Software","Software",
        "Software","Software","Software","Software",
        "Software","Software","Software","Software",

        # HARDWARE
        "Hardware","Hardware","Hardware","Hardware",
        "Hardware","Hardware","Hardware","Hardware",
        "Hardware","Hardware","Hardware","Hardware",

        # SYSTEM
        "System","System","System","System",
        "System","System","System","System",
        "System","System","System","System"
    ]
}

df = pd.DataFrame(data)

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            C=5
        )
    )
])

model.fit(df["ticket"], df["category"])

os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/ticket_classifier.pkl"
)

print("===================================")
print("SupportPilot Model Training")
print("===================================")
print("Training examples:", len(df))
print("Categories:", df["category"].unique())
print("Model trained successfully!")
print("Model saved at:")
print("models/ticket_classifier.pkl")
print("===================================")