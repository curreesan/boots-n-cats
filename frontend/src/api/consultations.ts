import { apiFetch } from "./apiFetch";

export async function createConsultation(
  petId: string,
  contact: string,
  preferredTime: string,
): Promise<void> {
  const response = await apiFetch("/adoption-consultations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      pet_id: petId,
      contact,
      preferred_time: preferredTime,
    }),
  });
  if (!response.ok) throw new Error("Failed to submit request");
}

export type Consultation = {
  id: string;
  user_id: string;
  pet_id: string;
  contact: string;
  preferred_time: string;
  status: string;
  created_at: string;
};

export async function getAdminConsultations(): Promise<Consultation[]> {
  const response = await apiFetch("/admin/adoption-consultations");
  if (!response.ok) throw new Error("Failed to fetch consultations");
  const data = await response.json();
  return data.items;
}
