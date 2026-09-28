from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from knowledge_base import knowledge_base


class KnowledgeRetriever:

    def __init__(self, documents):

        self.documents = documents

        # -----------------------------
        # TITLE TEXT
        # -----------------------------

        self.title_texts = [
            str(document["title"])
            for document in documents
        ]

        # -----------------------------
        # CONTENT TEXT
        # -----------------------------

        self.content_texts = [
            str(document["content"])
            for document in documents
        ]

        # -----------------------------
        # TF-IDF VECTORIZERS
        # -----------------------------

        self.title_vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        self.content_vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        # -----------------------------
        # CREATE VECTORS
        # -----------------------------

        self.title_vectors = self.title_vectorizer.fit_transform(
            self.title_texts
        )

        self.content_vectors = self.content_vectorizer.fit_transform(
            self.content_texts
        )


    # ==========================================
    # SEARCH KNOWLEDGE BASE
    # ==========================================

    def search(self, query, top_k=3):

        query = str(query)

        # -----------------------------
        # QUERY VECTORS
        # -----------------------------

        query_title_vector = self.title_vectorizer.transform(
            [query]
        )

        query_content_vector = self.content_vectorizer.transform(
            [query]
        )

        # -----------------------------
        # TITLE SIMILARITY
        # -----------------------------

        title_scores = cosine_similarity(
            query_title_vector,
            self.title_vectors
        )[0]

        # -----------------------------
        # CONTENT SIMILARITY
        # -----------------------------

        content_scores = cosine_similarity(
            query_content_vector,
            self.content_vectors
        )[0]

        # -----------------------------
        # FINAL SCORE
        # TITLE = 70%
        # CONTENT = 30%
        # -----------------------------

        final_scores = (
            0.7 * title_scores +
            0.3 * content_scores
        )

        # Highest score first

        ranked_indices = final_scores.argsort()[::-1]

        results = []

        for index in ranked_indices[:top_k]:

            results.append({

                "id": self.documents[index]["id"],

                "title": self.documents[index]["title"],

                "category": self.documents[index]["category"],

                "content": self.documents[index]["content"],

                "score": float(final_scores[index])

            })

        return results


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    retriever = KnowledgeRetriever(
        knowledge_base
    )

    query = "VPN connection timeout on corporate network"

    results = retriever.search(
        query,
        top_k=3
    )

    print("\nKnowledge Base Search Results")
    print("=" * 50)

    for result in results:

        print("ID:", result["id"])

        print("Title:", result["title"])

        print("Category:", result["category"])

        print(
            "Relevance Score:",
            round(result["score"], 2)
        )

        print("Content:")

        print(result["content"])

        print("-" * 50)