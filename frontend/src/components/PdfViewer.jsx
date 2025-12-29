import React, { useEffect, useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

export default function PdfViewer({ fileUrl, page }) {
  const [numPages, setNumPages] = useState(null);
  const [currentPage, setCurrentPage] = useState(page || 1);

  useEffect(() => {
    if (page) {
      setCurrentPage(page);
    }
  }, [page]);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

  if (!fileUrl) {
    return (
      <div className="panel">
        <h3>PDF Viewer</h3>
        <p>Upload a PDF to preview it here.</p>
      </div>
    );
  }

  return (
    <div className="panel">
      <h3>PDF Viewer</h3>
      <div className="pdf-container">
        <Document file={fileUrl} onLoadSuccess={onDocumentLoadSuccess}>
          <Page pageNumber={currentPage} />
        </Document>
      </div>
      <div className="pager">
        <button
          className="small-btn"
          onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
        >
          Prev
        </button>
        <span>
          Page {currentPage} / {numPages || "?"}
        </span>
        <button
          className="small-btn"
          onClick={() =>
            setCurrentPage((p) =>
              numPages ? Math.min(numPages, p + 1) : p + 1
            )
          }
        >
          Next
        </button>
      </div>
    </div>
  );
}
