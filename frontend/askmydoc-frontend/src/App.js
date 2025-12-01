import React, { useState } from "react";
import axios from "axios";
import "./App.css";  // <-- importer le CSS

function App() {
    const [file, setFile] = useState(null);
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");

    const uploadPDF = async () => {
        if (!file) return;
        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await axios.post("http://localhost:5000/upload_pdf", formData);
            alert(res.data.message);
        } catch (err) {
            console.error(err);
            alert("Erreur lors de l'upload");
        }
    };

    const askQuestion = async () => {
        try {
            const res = await axios.post("http://localhost:5000/ask", { question });
            setAnswer(res.data.answer);
        } catch (err) {
            console.error(err);
            alert("Erreur lors de la question");
        }
    };

    return (
        <div className="App">
            <h1>AskMyDoc PDF Assistant</h1>

            <div>
                <h3>Uploader PDF</h3>
                <input type="file" onChange={(e) => setFile(e.target.files[0])} />
                <button onClick={uploadPDF}>Upload</button>
            </div>

            <div style={{ marginTop: "20px" }}>
                <h3>Poser une question</h3>
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                />
                <button onClick={askQuestion}>Poser la question</button>
            </div>

            {answer && (
                <div className="answer-box">
                    <h3>Réponse :</h3>
                    <p>{answer}</p>
                </div>
            )}
        </div>
    );
}

export default App;
