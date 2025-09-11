import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class RAGPipeline:
    def __init__(
        self,
        embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        llm_model_name: str = "microsoft/phi-3-mini-128k-instruct",
        db_path: str = "./chroma_db",
        device: str = "cpu",  # or "cuda" if GPU is available
    ):
        """
        Initialize RAG pipeline whith,

        Sentence embeddings with MiniLM
        Local ChromaDB vector database
        Local Phi-3-mini-128k LLM
        """
        self.device = device
        self.embedder = SentenceTransformer(embedding_model_name)

        # ChromaDB setup
        settings = Settings(persist_directory=db_path)
        self.client = chromadb.Client(settings)

        # Create or get collection
        collections = self.client.list_collections()
        if "co2_rag" in [c.name for c in collections]:
            self.collection = self.client.get_collection("co2_rag")
        else:
            self.collection = self.client.create_collection("co2_rag")

        # Load local LLM
        self.tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
        self.model = AutoModelForCausalLM.from_pretrained(llm_model_name)
        self.model.to(self.device)
        self.model.eval()

    def load_data(self, csv_path: str, doc_path: str):
        """
        Load CSV and document, create embeddings, and store them in ChromaDB.
        """
        df = pd.read_csv(csv_path)

        # Convert csv rows into descriptive text
        records = [
            f"Date: {row['date']} | Facility: {row['facility_name']} ({row['facility_id']}) "
            f"in {row['region']}, {row['country']} | Storage Type: {row['storage_site_type']} | "
            f"CO2 Emitted: {row['co2_emitted_tonnes']} tonnes | "
            f"CO2 Captured: {row['co2_captured_tonnes']} tonnes | "
            f"CO2 Stored: {row['co2_stored_tonnes']} tonnes | "
            f"Capture Efficiency: {row['capture_efficiency_percent']}% | "
            f"Storage Integrity: {row['storage_integrity_percent']}% | "
            f"Anomaly: {row['anomaly_flag']} | Notes: {row['notes']} | "
            f"Season: {row['season']}"
            for _, row in df.iterrows()
        ]

        # Load and chunk document
        with open(doc_path, "r", encoding="utf-8") as f:
            doc_text = f.read()

        doc_chunks = [doc_text[i:i+500] for i in range(0, len(doc_text), 500)]

        # Combine CSV + document chunks
        all_chunks = records + doc_chunks

        # Create embeddings
        embeddings = self.embedder.encode(all_chunks, show_progress_bar=False)

        # Add to ChromaDB
        for i, chunk in enumerate(all_chunks):
            self.collection.add(
                documents=[chunk],
                embeddings=[embeddings[i].tolist()],
                ids=[str(i)]
            )

    def retrieve(self, query: str, k: int = 5):
        """
        Retrieve top-k relevant chunks for a query.
        """
        q_emb = self.embedder.encode([query])[0]
        results = self.collection.query(
            query_embeddings=[q_emb.tolist()],
            n_results=k
        )
        return results['documents'][0]

    def answer_question(self, query: str, max_new_tokens: int = 300) -> str:
        
        #This will generate a text using a local Phi 3 mini 128k.
        
        context = "\n".join(self.retrieve(query))
        prompt = f"""
You are an assistant answering questions about CO₂ capture.

Context:
{context}

Question: {query}
Answer:
"""

        # Tokenize and move to device
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        # Generate output
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
