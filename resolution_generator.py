from retriever import KnowledgeRetriever
from knowledge_base import knowledge_base


def generate_resolution(ticket, retrieved_docs):

    if not retrieved_docs:
        return "No relevant knowledge-base information was found."

    resolution = []

    resolution.append("Recommended Troubleshooting Steps:")

    step_number = 1

    for doc in retrieved_docs:

        lines = doc["content"].split("\n")

        for line in lines:

            line = line.strip()

            # Check for numbered steps
            if len(line) >= 3 and line[0].isdigit() and line[1] == ".":

                step = line.split(".", 1)[1].strip()

                resolution.append(
                    f"{step_number}. {step}"
                )

                step_number += 1

    resolution.append("")
    resolution.append(
        "If the issue persists, please contact the IT support team."
    )

    return "\n".join(resolution)


# --------------------------------
# TEST RESOLUTION GENERATOR
# --------------------------------

if __name__ == "__main__":

    retriever = KnowledgeRetriever(knowledge_base)

    ticket = """
    VPN is not connecting.
    I cannot access the company network.
    """

    results = retriever.search(
        ticket,
        top_k=2
    )

    resolution = generate_resolution(
        ticket,
        results
    )

    print("\nGenerated Resolution")
    print("=" * 50)
    print(resolution)