from langchain_chroma import Chroma


def store_embeddings(chunks, embedding_model):
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="vectorstore"
    )
    return vectorstore


def get_retriever(embedding_model):
    vectorstore = Chroma(
        persist_directory="vectorstore",
        embedding_function=embedding_model
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",   # 🔥 IMPORTANT
        search_kwargs={
            "k": 3,
            "fetch_k": 6     # fetch more, then diversify
        }
    )

    return retriever

def retrieve_docs(query, retriever):
    results = retriever.invoke(query)

    # remove duplicates
    unique = []
    seen = set()

    for doc in results:
        content = doc.page_content.strip()
        if content not in seen:
            seen.add(content)
            unique.append(doc)

    return unique