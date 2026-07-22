import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import ChatWidget from "./ChatWidget";
import "../styles/Layout.css";

function Layout() {
  return (
    <div>
      <Navbar />
      <main className="layout__content">
        <Outlet />
      </main>
      <ChatWidget />
    </div>
  );
}

export default Layout;
