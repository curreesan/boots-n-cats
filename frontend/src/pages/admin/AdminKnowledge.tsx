import { useState, useEffect } from "react";
import {
  uploadKnowledgeDoc,
  getKnowledgeDocs,
  type KnowledgeDoc,
} from "../../api/knowledge";
import "../../styles/AdminForm.css";

function AdminKnowledge() {
  const [docs, setDocs] = useState<KnowledgeDoc[]>([]);
  const [loading, setLoading] = useState(true);
  const [file, setFile] = useState<File | null>(null);
  const [documentType, setDocumentType] = useState("care_guide");
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function loadDocs() {
    const data = await getKnowledgeDocs();
    setDocs(data);
    setLoading(false);
  }

  useEffect(() => {
    // loadDocs fetches from our backend and is reused by handleUpload to
    // refresh the list after a new document is ingested — a legitimate
    // external sync, not a derived-state anti-pattern.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void loadDocs();
  }, []);

  async function handleUpload(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setError(null);
    try {
      await uploadKnowledgeDoc(file, documentType);
      setFile(null);
      await loadDocs();
    } catch {
      setError("Upload failed");
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="admin-section">
      <h2 className="admin-section__heading">Knowledge Documents</h2>

      <form className="admin-form" onSubmit={handleUpload}>
        <input
          type="file"
          accept=".txt,.pdf"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          required
        />
        <select
          value={documentType}
          onChange={(e) => setDocumentType(e.target.value)}
        >
          <option value="care_guide">Care Guide</option>
          <option value="adoption_policy">Adoption Policy</option>
          <option value="faq">FAQ</option>
        </select>
        <button
          type="submit"
          className="admin-form__submit"
          disabled={uploading}
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>
      </form>

      {error && <div>{error}</div>}

      {loading ? (
        <div className="admin-section__status">Loading...</div>
      ) : (
        <div className="admin-section__list">
          {docs.map((doc) => (
            <div key={doc.id} className="admin-section__row">
              <span>
                {doc.filename} — {doc.document_type} — {doc.status} (
                {doc.chunk_count} chunks)
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AdminKnowledge;
