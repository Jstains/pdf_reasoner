import React, { useState } from "react";
import { uploadPdf } from "../api";

export default function Upload({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF file.");
      return;
    }
    setStatus("Uploading and indexing PDF...");
    try {
      const { data, pdfUrl } = await uploadPdf(file);
      setStatus(`Uploaded: ${data.filename} (${data.pages} pages)`);
      onUploaded(data, pdfUrl);
    } catch (err) {
      console.error(err);
      setStatus("Upload failed.");
      alert("Upload or ingestion failed. Check backend logs.");
    }
  };

  return (
    <div className="panel">
      <h3>1) Upload PDF</h3>
      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0] || null)}
      />
      <button onClick={handleUpload}>Upload & Index</button>
      {status && <div className="status">{status}</div>}
    </div>
  );
}
