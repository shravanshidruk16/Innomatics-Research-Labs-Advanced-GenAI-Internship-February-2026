from ingestion.loader import load_pdf
from ingestion.chunker import chunk_documents
from ingestion.embedder import get_embedding_model
from retrieval.retriever import store_embeddings, get_retriever
from llm.llm import get_llm
from graph.workflow import build_graph


def setup_pipeline():
    print("🔄 Setting up RAG pipeline...")

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

    print("✅ Setup complete!\n")
    return retriever, llm


def run_chatbot(retriever, llm):
    graph = build_graph()

    print("🤖 NovaTech Support Assistant Ready!")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("👤 You: ")

        if query.lower() in ["exit", "quit"]:
            print("👋 Exiting chatbot...")
            break

        result = graph.invoke({
            "query": query,
            "retriever": retriever,
            "llm": llm
        })

        print("\n🤖 Assistant:")
        print(result["answer"])
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    retriever, llm = setup_pipeline()
    run_chatbot(retriever, llm)