import { API_BASE_URL } from "./config";

export async function createConsultation(
  petId: string,
  contact: string,
  preferredTime: string,
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/adoption-consultations`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      pet_id: petId,
      contact,
      preferred_time: preferredTime,
    }),
  });
  if (!response.ok) throw new Error("Failed to submit request");
}
