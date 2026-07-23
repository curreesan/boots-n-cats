import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/useAuth";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

function Account() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  if (!user)
    return <div className="py-12 text-muted-foreground">Not logged in.</div>;

  async function handleLogout() {
    await logout();
    navigate("/login");
  }

  return (
    <div className="flex flex-col gap-6 py-10">
      <h1 className="text-3xl font-bold">Account</h1>

      <Card className="max-w-md gap-0 py-0">
        <CardContent className="divide-y divide-border p-0">
          <div className="flex items-center justify-between px-6 py-4">
            <span className="text-sm font-medium text-muted-foreground">
              Name
            </span>
            <span>{user.name}</span>
          </div>
          <div className="flex items-center justify-between px-6 py-4">
            <span className="text-sm font-medium text-muted-foreground">
              Email
            </span>
            <span>{user.email}</span>
          </div>
          <div className="flex items-center justify-between px-6 py-4">
            <span className="text-sm font-medium text-muted-foreground">
              Role
            </span>
            <span className="capitalize">{user.role}</span>
          </div>
        </CardContent>
      </Card>

      <Button
        variant="outline"
        className="w-fit border-destructive text-destructive hover:bg-destructive hover:text-white"
        onClick={handleLogout}
      >
        Logout
      </Button>
    </div>
  );
}

export default Account;
