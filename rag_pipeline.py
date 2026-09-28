from retriever import KnowledgeRetriever
from knowledge_base import knowledge_base
from context_builder import build_context
from resolution_generator import generate_resolution


# Create retriever
retriever = KnowledgeRetriever(knowledge_base)


def run_rag_pipeline(ticket):

    # Step 1: Retrieve relevant documents
    retrieved_docs = retriever.search(
        ticket,
        top_k=2
    )

    # Step 2: Build context
    context = build_context(
        retrieved_docs
    )

    # Step 3: Generate resolution
    resolution = generate_resolution(
        ticket,
        retrieved_docs
    )

    return {
        "retrieved_docs": retrieved_docs,
        "context": context,
        "resolution": resolution
    }


# --------------------------------
# TEST COMPLETE RAG PIPELINE
# --------------------------------

if __name__ == "__main__":

    ticket = """
    VPN is not connecting.
    I cannot access the company network.
    """

    result = run_rag_pipeline(ticket)

    print("\n")
    print("=" * 60)
    print("SUPPORTPILOT RAG PIPELINE")
    print("=" * 60)

    print("\nRETRIEVED DOCUMENTS")
    print("-" * 60)

    for doc in result["retrieved_docs"]:

        print("ID:", doc["id"])
        print("Title:", doc["title"])
        print("Category:", doc["category"])
        print(
            "Relevance Score:",
            round(doc["score"], 2)
        )
        print()

    print("\nCONTEXT")
    print("-" * 60)
    print(result["context"])

    print("\nGENERATED RESOLUTION")
    print("-" * 60)
    print(result["resolution"])