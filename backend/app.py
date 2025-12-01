from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile
import os

# ----------------------------
# Flask app
# ----------------------------
app = Flask(__name__)
CORS(app)

vector_store = None
qa_chain = None

# ----------------------------
# Endpoint : Upload PDF
# ----------------------------
@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    global vector_store, qa_chain

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Aucun fichier reçu"}), 400

    # Sauvegarde temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        file.save(temp.name)
        pdf_path = temp.name

    # Charger PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Splitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    # Embeddings via Ollama (GRATUIT)
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    # Vector store FAISS
    vector_store = FAISS.from_documents(docs, embeddings)

    # Modèle LLM (gratuit via Ollama)
    llm = Ollama(model="llama3")

    # RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_store.as_retriever(),
        chain_type="stuff"
    )

    return jsonify({"message": "PDF chargé et indexé avec succès"})


# ----------------------------
# Endpoint : Ask question
# ----------------------------
@app.route("/ask", methods=["POST"])
def ask_question():
    global qa_chain

    data = request.get_json()
    question = data.get("question")

    if not qa_chain:
        return jsonify({"error": "Aucun document chargé"}), 400

    response = qa_chain.invoke({"query": question})

    return jsonify({"answer": response["result"]})


# ----------------------------
# Lancer le serveur
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
