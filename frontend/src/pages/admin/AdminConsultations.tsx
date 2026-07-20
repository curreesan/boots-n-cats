import { useState, useEffect } from "react";
import { API_BASE_URL } from "../../api/config";
import "../../styles/AdminConsultations.css";

type Consultation = {
  id: string;
  user_id: string;
  pet_id: string;
  contact: string;
  preferred_time: string;
  status: string;
  created_at: string;
};

function AdminConsultations() {
  const [consultations, setConsultations] = useState<Consultation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const response = await fetch(
        `${API_BASE_URL}/admin/adoption-consultations`,
        {
          credentials: "include",
        },
      );
      const data = await response.json();
      setConsultations(data);
      setLoading(false);
    }
    void load();
  }, []);

  if (loading)
    return <div className="admin-consultations__status">Loading...</div>;

  return (
    <div className="admin-consultations">
      <h1 className="admin-consultations__heading">Consultation Requests</h1>

      {consultations.length === 0 ? (
        <div className="admin-consultations__status">No requests yet.</div>
      ) : (
        <div className="admin-consultations__list">
          {consultations.map((c) => (
            <div key={c.id} className="admin-consultations__row">
              <span className="admin-consultations__contact">{c.contact}</span>
              <span className="admin-consultations__time">
                {c.preferred_time}
              </span>
              <span className="admin-consultations__date">
                {new Date(c.created_at).toLocaleString()}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AdminConsultations;
