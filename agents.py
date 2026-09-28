
import json
import os
import re
import math

from collections import Counter


# =========================================================
# KNOWLEDGE BASE LOADER
# =========================================================

class KnowledgeBaseLoader:

    def __init__(self, file_path=None):

        if file_path is None:
            file_path = os.path.join(
                os.path.dirname(__file__),
                "knowledge_base",
                "knowledge.json"
            )

        self.file_path = file_path
        self.knowledge_base = self.load_knowledge_base()

    def load_knowledge_base(self):

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            print(
                f"Knowledge base loaded: {len(data)} articles"
            )

            return data

        except FileNotFoundError:

            print(
                "ERROR: knowledge.json file not found."
            )

            return []

        except json.JSONDecodeError:

            print(
                "ERROR: Invalid JSON format."
            )

            return []


# =========================================================
# AGENT 1: DIAGNOSIS AGENT
# =========================================================

class DiagnosisAgent:

    def __init__(self):

        self.category_keywords = {

            "Network": [
                "vpn",
                "network",
                "internet",
                "connection",
                "connectivity"
            ],

            "Authentication": [
                "password",
                "login",
                "authentication",
                "account",
                "credential"
            ],

            "Email": [
                "email",
                "outlook",
                "mailbox",
                "mail"
            ],

            "Printer": [
                "printer",
                "printing",
                "print"
            ],

            "Performance": [
                "slow",
                "performance",
                "cpu",
                "memory",
                "lag"
            ]

        }

    def diagnose(self, ticket_text):

        text = ticket_text.lower()

        for category, keywords in self.category_keywords.items():

            for keyword in keywords:

                pattern = (
                    r"\b"
                    + re.escape(keyword)
                    + r"\b"
                )

                if re.search(pattern, text):

                    return {

                        "category": category,

                        "issue": ticket_text,

                        "confidence": 0.80,

                        "message": (
                            "Issue category identified successfully."
                        )

                    }

        return {

            "category": "General IT Issue",

            "issue": ticket_text,

            "confidence": 0.50,

            "message": (
                "Unable to identify a specific category."
            )

        }


# =========================================================
# AGENT 2: RETRIEVAL AGENT
# =========================================================

class RetrievalAgent:

    def __init__(self, knowledge_base):

        self.knowledge_base = knowledge_base

        self.documents = [

            item.get("content", "")

            for item in knowledge_base

        ]

    def tokenize(self, text):

        words = re.findall(
            r"\b[a-zA-Z]+\b",
            text.lower()
        )

        stop_words = {

            "the",
            "is",
            "a",
            "an",
            "and",
            "or",
            "to",
            "of",
            "in",
            "your",
            "for",
            "on",
            "with",
            "my",
            "i",
            "cannot",
            "not"

        }

        return [

            word

            for word in words

            if word not in stop_words

        ]

    def calculate_similarity(self, query, document):

        query_words = self.tokenize(query)

        document_words = self.tokenize(document)

        query_count = Counter(query_words)

        document_count = Counter(document_words)

        common_words = set(
            query_count.keys()
        ).intersection(
            set(document_count.keys())
        )

        dot_product = sum(

            query_count[word]
            * document_count[word]

            for word in common_words

        )

        query_magnitude = math.sqrt(

            sum(

                value ** 2

                for value in query_count.values()

            )

        )

        document_magnitude = math.sqrt(

            sum(

                value ** 2

                for value in document_count.values()

            )

        )

        if (

            query_magnitude == 0

            or document_magnitude == 0

        ):

            return 0.0

        similarity = (

            dot_product

            / (

                query_magnitude
                * document_magnitude

            )

        )

        return similarity

    def retrieve(self, query):

        if not self.documents:

            return {

                "article": None,

                "similarity": 0.0,

                "message": (
                    "Knowledge base is empty."
                )

            }

        similarity_scores = []

        for document in self.documents:

            score = self.calculate_similarity(

                query,

                document

            )

            similarity_scores.append(score)

        best_index = similarity_scores.index(

            max(similarity_scores)

        )

        best_score = float(

            similarity_scores[best_index]

        )

        best_article = self.knowledge_base[best_index]

        return {

            "article": best_article,

            "similarity": best_score,

            "message": (
                "Relevant knowledge article retrieved."
            )

        }


# =========================================================
# AGENT 3: RESOLUTION AGENT
# =========================================================

class ResolutionAgent:

    def generate_resolution(
        self,
        diagnosis,
        retrieval
    ):

        category = diagnosis.get(
            "category",
            "General IT Issue"
        )

        article = retrieval.get("article")

        if article is None:

            steps = [

                "Collect more information about the issue.",

                "Contact the IT support team for assistance."

            ]

            response = (

                "We need more information to identify "
                "the issue. Please contact the IT support team."

            )

            return {

                "steps": steps,

                "response": response

            }

        if category == "Network":

            steps = [

                "Check your internet connection.",

                "Restart the VPN client.",

                "Verify your username and password.",

                "Clear the VPN cache.",

                "Restart your computer.",

                "Check firewall and network configuration."

            ]

        elif category == "Authentication":

            steps = [

                "Open the company password portal.",

                "Click on Forgot Password.",

                "Verify your identity.",

                "Create a new password.",

                "Confirm the new password.",

                "Try logging in again."

            ]

        elif category == "Email":

            steps = [

                "Check your internet connection.",

                "Check mailbox storage.",

                "Restart Outlook.",

                "Remove and re-add the email account.",

                "Verify email server settings."

            ]

        elif category == "Printer":

            steps = [

                "Check whether the printer is powered on.",

                "Verify the printer connection.",

                "Check the paper and ink.",

                "Clear pending print jobs.",

                "Restart the printer and computer."

            ]

        elif category == "Performance":

            steps = [

                "Restart the computer.",

                "Close unnecessary applications.",

                "Check CPU and memory usage.",

                "Remove temporary files.",

                "Scan the computer for malware.",

                "Update system software."

            ]

        else:

            content = article.get(
                "content",
                ""
            )

            steps = [

                sentence.strip()

                for sentence in content.split(".")

                if sentence.strip()

            ]

        response = (

            f"We identified the issue as {category}.\n"

            "Please follow these troubleshooting steps:\n\n"

        )

        for index, step in enumerate(

            steps,

            start=1

        ):

            response += (

                f"{index}. {step}\n"

            )

        return {

            "steps": steps,

            "response": response

        }


# =========================================================
# AGENT 4: VALIDATION AGENT
# =========================================================

class ValidationAgent:

    def validate(

        self,

        diagnosis,

        retrieval,

        resolution

    ):

        diagnosis_confidence = float(

            diagnosis.get(

                "confidence",

                0.0

            )

        )

        retrieval_similarity = float(

            retrieval.get(

                "similarity",

                0.0

            )

        )

        steps = resolution.get(

            "steps",

            []

        )

        step_completeness = min(

            len(steps) / 6,

            1

        )

        final_confidence = (

            diagnosis_confidence * 0.40

            + retrieval_similarity * 0.40

            + step_completeness * 0.20

        )

        confidence_percentage = round(

            final_confidence * 100,

            2

        )

        if confidence_percentage >= 70:

            status = "AUTO_RESOLVE"

        else:

            status = "ESCALATE"

        return {

            "diagnosis_confidence": round(

                diagnosis_confidence * 100,

                2

            ),

            "retrieval_similarity": round(

                retrieval_similarity * 100,

                2

            ),

            "step_completeness": round(

                step_completeness * 100,

                2

            ),

            "final_confidence": confidence_percentage,

            "status": status

        }


# =========================================================
# AGENT 5: ESCALATION AGENT
# =========================================================

class EscalationAgent:

    def check_escalation(

        self,

        validation_result

    ):

        status = validation_result.get(

            "status"

        )

        if status == "ESCALATE":

            return {

                "required": True,

                "message": (

                    "This ticket requires manual review "
                    "by the IT support team."

                )

            }

        return {

            "required": False,

            "message": (

                "The ticket has sufficient confidence "
                "for automatic resolution."

            )

        }


# =========================================================
# SUPPORTPILOT ORCHESTRATOR
# =========================================================

class SupportPilot:

    def __init__(self):

        knowledge_loader = KnowledgeBaseLoader()

        self.knowledge_base = (

            knowledge_loader.knowledge_base

        )

        self.diagnosis_agent = DiagnosisAgent()

        self.retrieval_agent = RetrievalAgent(

            self.knowledge_base

        )

        self.resolution_agent = ResolutionAgent()

        self.validation_agent = ValidationAgent()

        self.escalation_agent = EscalationAgent()

    def process_ticket(self, ticket_text):

        print("\nStarting ticket processing...")

        # Step 1: Diagnosis
        diagnosis_result = (

            self.diagnosis_agent.diagnose(

                ticket_text

            )

        )

        # Step 2: Retrieval
        retrieval_result = (

            self.retrieval_agent.retrieve(

                ticket_text

            )

        )

        # Step 3: Resolution
        resolution_result = (

            self.resolution_agent.generate_resolution(

                diagnosis_result,

                retrieval_result

            )

        )

        # Step 4: Validation
        validation_result = (

            self.validation_agent.validate(

                diagnosis_result,

                retrieval_result,

                resolution_result

            )

        )

        # Step 5: Escalation
        escalation_result = (

            self.escalation_agent.check_escalation(

                validation_result

            )

        )

        print("Ticket processing completed.")

        return {

            "diagnosis": diagnosis_result,

            "retrieval": retrieval_result,

            "resolution": resolution_result,

            "validation": validation_result,

            "escalation": escalation_result

        }


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    print(
        "\n========================================"
    )

    print(
        "SupportPilot Agent System Started"
    )

    print(
        "========================================"
    )

    test_ticket = (

        "My VPN is not working and I cannot "
        "connect to the company network."

    )

    support_pilot = SupportPilot()

    result = support_pilot.process_ticket(

        test_ticket

    )

    print(
        "\n========== DIAGNOSIS =========="
    )

    print(

        result["diagnosis"]

    )

    print(
        "\n========== RETRIEVAL =========="
    )

    print(

        result["retrieval"]

    )

    print(
        "\n========== RESOLUTION =========="
    )

    print(

        result["resolution"]["response"]

    )

    print(
        "\n========== VALIDATION =========="
    )

    print(

        result["validation"]

    )

    print(
        "\n========== ESCALATION =========="
    )

    print(

        result["escalation"]

    )

    print(
        "\n========================================"
    )

    print(
        "SupportPilot Agent System Completed"
    )

    print(
        "========================================"
    )