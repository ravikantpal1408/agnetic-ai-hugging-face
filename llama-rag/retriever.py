# retriever.py
from typing import Any, Dict

import datasets
from langchain_core.documents import Document


def load_and_prepare_dataset():
    print("Loading guest dataset from Hugging Face...")
    guest_dataset = datasets.load_dataset("agents-course/unit3-invitees", split="train")

    # We explicitly declare each row as a Dict so Pyright allows string indexing
    docs = []
    for guest in guest_dataset:
        row: Dict[str, Any] = guest  # type: ignore
        docs.append(
            Document(
                page_content="\n".join(
                    [
                        f"Name: {row.get('name')}",
                        f"Relation: {row.get('relation')}",
                        f"Description: {row.get('description')}",
                        f"Email: {row.get('email')}",
                    ]
                ),
                metadata={"name": row.get("name", "")},
            )
        )

    return docs
