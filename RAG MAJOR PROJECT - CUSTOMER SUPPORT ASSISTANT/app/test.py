from ingestion.loader import load_pdf
from ingestion.chunker import chunk_documents
from ingestion.embedder import get_embedding_model
from retrieval.retriever import store_embeddings, get_retriever, retrieve_docs
from llm.llm import get_llm
from graph.workflow import build_graph


def setup_pipeline():
    # Load and process document
    docs = load_pdf("data/knowledge_base.pdf")
    chunks = chunk_documents(docs)

    # Embeddings + Vector DB
    embedding_model = get_embedding_model()
    store_embeddings(chunks, embedding_model)

    # Retriever
    retriever = get_retriever(embedding_model)

    # LLM
    llm = get_llm()

    return retriever, llm


def test_retrieval(retriever):
    query = "What is HTTP?"
    results = retrieve_docs(query, retriever)

    print("\nRetrieved Chunks:\n")
    for i, doc in enumerate(results):
        print(f"\n--- Chunk {i+1} ---")
        print(doc.page_content[:300])


def test_llm(retriever, llm):
    query = "What is HTTP?"
    results = retrieve_docs(query, retriever)

    context = "\n".join([doc.page_content for doc in results])

    prompt = f"""
    Answer the question based ONLY on the context below.

    Context:
    {context}

    Question:
    {query}
    """

    response = llm.invoke(prompt)

    print("\nLLM Answer:\n")
    print(response.content)


def test_graph(retriever, llm):
    graph = build_graph()

    result = graph.invoke({
        "query": "What is HTTP?",
        "retriever": retriever,
        "llm": llm
    })

    print("\nGraph Final Answer:\n")
    print(result["answer"])


if __name__ == "__main__":
    retriever, llm = setup_pipeline()

    # Step-by-step testing (important)
    test_retrieval(retriever)
    test_llm(retriever, llm)
    test_graph(retriever, llm)