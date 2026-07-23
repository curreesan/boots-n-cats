import { apiFetch } from "./apiFetch";

export type KnowledgeDoc = {
  id: string;
  filename: string;
  document_type: string;
  status: string;
  chunk_count: number;
};

export async function uploadKnowledgeDoc(file: File, documentType: string) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("document_type", documentType);

  const response = await apiFetch("/admin/knowledge/upload", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) throw new Error("Upload failed");
  return response.json();
}

export async function getKnowledgeDocs(): Promise<KnowledgeDoc[]> {
  const response = await apiFetch("/admin/knowledge");
  if (!response.ok) throw new Error("Failed to fetch documents");
  return response.json();
}
