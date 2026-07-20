import { Link } from "react-router-dom";
import { useAuth } from "../context/useAuth";
import "../styles/Navbar.css";

function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar__inner">
        <Link to="/" className="navbar__brand">
          Boots n' Cats
        </Link>

        <div className="navbar__links">
          {user && user.role === "staff" && (
            <>
              <Link to="/admin/catalog">Admin: Catalog</Link>
              <Link to="/admin/consultations">Admin: Requests</Link>
            </>
          )}

          <Link to="/">Home</Link>
          <Link to="/products">Products</Link>
          <Link to="/pets">Pets</Link>
          <Link to="/cart">Cart</Link>

          {user ? (
            <>
              <Link to="/orders">Orders</Link>
              <Link to="/account">Woof Meow, {user.name}</Link>
              <button onClick={() => logout()}>Logout</button>
            </>
          ) : (
            <>
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
