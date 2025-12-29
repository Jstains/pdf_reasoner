import React, { useState } from "react";
import Upload from "./components/Upload";
import Chat from "./components/Chat";
import PdfViewer from "./components/PdfViewer";

function App() {
  const [doc, setDoc] = useState(null); // { doc_id, filename, pages }
  const [pdfUrl, setPdfUrl] = useState(null);
  const [openPage, setOpenPage] = useState(null);

  return (
    <div className="container">
      <h1>Agent-Based PDF Reasoner</h1>
      <p className="subtitle">
        LangChain Agent + Gemini + Page-aware PDF Q&A with citations
      </p>

      <div className="layout">
        <div className="left">
          <Upload
            onUploaded={(docInfo, url) => {
              setDoc(docInfo);
              setPdfUrl(url);
              setOpenPage(1);
            }}
          />
          <Chat doc={doc} onOpenPage={setOpenPage} />
        </div>
        <div className="right">
          <PdfViewer fileUrl={pdfUrl} page={openPage} />
        </div>
      </div>
    </div>
  );
}

export default App;
