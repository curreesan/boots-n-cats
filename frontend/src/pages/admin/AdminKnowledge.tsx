import { useState, useEffect } from "react";
import {
  uploadKnowledgeDoc,
  getKnowledgeDocs,
  type KnowledgeDoc,
} from "../../api/knowledge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

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
    <div className="py-10">
      <Card>
        <CardHeader>
          <CardTitle>Knowledge Documents</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-6">
          <form
            className="flex flex-wrap items-center gap-3 border-b border-border pb-6"
            onSubmit={handleUpload}
          >
            <input
              type="file"
              accept=".txt,.pdf"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
              required
              className="text-sm"
            />
            <select
              className="h-9 rounded-md border border-input bg-transparent px-3 text-sm"
              value={documentType}
              onChange={(e) => setDocumentType(e.target.value)}
            >
              <option value="care_guide">Care Guide</option>
              <option value="adoption_policy">Adoption Policy</option>
              <option value="faq">FAQ</option>
            </select>
            <Button type="submit" disabled={uploading}>
              {uploading ? "Uploading..." : "Upload"}
            </Button>
          </form>

          {error && <p className="text-sm text-destructive">{error}</p>}

          {loading ? (
            <p className="text-sm text-muted-foreground">Loading...</p>
          ) : (
            <div className="divide-y divide-border overflow-hidden rounded-lg border border-border">
              {docs.map((doc) => (
                <div key={doc.id} className="px-4 py-3 text-sm">
                  {doc.filename} — {doc.document_type} — {doc.status} (
                  {doc.chunk_count} chunks)
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

export default AdminKnowledge;
