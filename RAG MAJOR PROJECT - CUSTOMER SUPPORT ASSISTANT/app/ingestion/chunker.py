from langchain_text_splitters import RecursiveCharacterTextSplitter
import re


def clean_text(text: str) -> str:
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    # Optional: remove excessive separators if any
    text = re.sub(r'\|+', ' ', text)

    return text.strip()


def chunk_documents(documents):
    # Clean documents
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,        # slightly smaller for better precision
        chunk_overlap=150,
        separators=[
            "\n\n",   # paragraph
            "\n",     # line
            ". ",     # sentence
            " ",      # word
        ]
    )

    chunks = text_splitter.split_documents(documents)
    return chunks