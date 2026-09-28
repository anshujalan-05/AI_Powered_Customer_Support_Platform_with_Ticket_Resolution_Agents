from retriever import KnowledgeRetriever
from knowledge_base import knowledge_base


def build_context(results):

    context = ""

    for result in results:

        context += f"""
Knowledge Base Article
----------------------
ID: {result['id']}
Title: {result['title']}
Category: {result['category']}
Relevance Score: {result['score']:.2f}

Content:
{result['content']}

----------------------
"""

    return context


# --------------------------------
# TEST CONTEXT BUILDER
# --------------------------------

if __name__ == "__main__":

    retriever = KnowledgeRetriever(knowledge_base)

    query = "VPN connection timeout on corporate network"

    results = retriever.search(
        query,
        top_k=2
    )

    context = build_context(results)

    print("\nGenerated Context")
    print("=" * 50)
    print(context)