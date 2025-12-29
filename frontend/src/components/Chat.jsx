import React, { useState } from "react";
import { askQuestion } from "../api";

export default function Chat({ doc, onOpenPage }) {
  const [question, setQuestion] = useState("");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    if (!doc) {
      alert("Upload a PDF first.");
      return;
    }
    if (!question.trim()) return;

    setLoading(true);
    try {
      const resp = await askQuestion(question, doc.doc_id, 5);
      const item = {
        question,
        answer: resp.answer,
        sources: resp.sources || [],
      };
      setHistory((prev) => [item, ...prev]);
      setQuestion("");
    } catch (err) {
      console.error(err);
      alert("Error asking question. Check backend logs.");
    }
    setLoading(false);
  };

  return (
    <div className="panel">
      <h3>2) Ask Questions</h3>
      <textarea
        rows={3}
        placeholder="Ask something about the uploaded PDF..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={submit} disabled={loading || !doc}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      <div className="history">
        {history.map((item, idx) => (
          <div key={idx} className="qa-block">
            <div className="q">
              <strong>Q:</strong> {item.question}
            </div>
            <div className="a">
              <strong>A:</strong> {item.answer}
            </div>
            {item.sources.length > 0 && (
              <div className="sources">
                <strong>Sources:</strong>
                <ul>
                  {item.sources.map((s, j) => (
                    <li key={j}>
                      Page {s.page} &mdash; score {s.score.toFixed(3)}<br />
                      <span className="snippet">
                        {s.text.slice(0, 150)}...
                      </span>
                      <button
                        className="small-btn"
                        onClick={() => onOpenPage(s.page)}
                      >
                        Open page
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
