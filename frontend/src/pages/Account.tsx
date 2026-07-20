import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/useAuth";
import "../styles/Account.css";

function Account() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  if (!user) return <div className="account__status">Not logged in.</div>;

  async function handleLogout() {
    await logout();
    navigate("/login");
  }

  return (
    <div className="account">
      <h1 className="account__heading">Account</h1>

      <div className="account__card">
        <div className="account__row">
          <span className="account__label">Name</span>
          <span>{user.name}</span>
        </div>
        <div className="account__row">
          <span className="account__label">Email</span>
          <span>{user.email}</span>
        </div>
        <div className="account__row">
          <span className="account__label">Role</span>
          <span>{user.role}</span>
        </div>
      </div>

      <button className="account__logout" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
}

export default Account;
