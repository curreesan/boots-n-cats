import { useState, useEffect } from "react";
import { getAdminConsultations, type Consultation } from "../../api/consultations";
import { Card } from "@/components/ui/card";

function AdminConsultations() {
  const [consultations, setConsultations] = useState<Consultation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const data = await getAdminConsultations();
      setConsultations(data);
      setLoading(false);
    }
    void load();
  }, []);

  if (loading)
    return <div className="py-12 text-muted-foreground">Loading...</div>;

  return (
    <div className="flex flex-col gap-6 py-10">
      <h1 className="text-3xl font-bold">Consultation Requests</h1>

      {consultations.length === 0 ? (
        <p className="text-muted-foreground">No requests yet.</p>
      ) : (
        <Card className="gap-0 overflow-hidden py-0">
          {consultations.map((c, i) => (
            <div
              key={c.id}
              className={`flex items-center justify-between px-6 py-4 text-sm ${
                i !== consultations.length - 1 ? "border-b border-border" : ""
              }`}
            >
              <span className="font-medium">{c.contact}</span>
              <span className="text-muted-foreground">{c.preferred_time}</span>
              <span className="text-muted-foreground">
                {new Date(c.created_at).toLocaleString()}
              </span>
            </div>
          ))}
        </Card>
      )}
    </div>
  );
}

export default AdminConsultations;
