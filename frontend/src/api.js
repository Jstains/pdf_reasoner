import axios from "axios";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000/api";
const API_UPLOAD_BASE = process.env.REACT_APP_API_UPLOAD_BASE || "http://localhost:8000";

export async function uploadPdf(file) {
  const fd = new FormData();
  fd.append("file", file);

  const resp = await axios.post(`${API_BASE}/upload`, fd, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  // Build URL to view the PDF directly from FastAPI static mount
  const pdfUrl = `${API_UPLOAD_BASE}/uploads/${resp.data.doc_id}.pdf`;
  return { data: resp.data, pdfUrl };
}

export async function askQuestion(question, docId, top_k = 5) {
  const resp = await axios.post(`${API_BASE}/qa`, {
    question,
    doc_id: docId,
    top_k,
  });
  return resp.data;
}
