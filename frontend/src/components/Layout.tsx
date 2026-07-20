import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import "../styles/Layout.css";

function Layout() {
  return (
    <div>
      <Navbar />
      <main className="layout__content">
        <Outlet />
      </main>
    </div>
  );
}

export default Layout;
