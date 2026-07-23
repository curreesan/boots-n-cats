import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import ChatWidget from "./ChatWidget";

function Layout() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="mx-auto max-w-6xl px-6">
        <Outlet />
      </main>
      <ChatWidget />
    </div>
  );
}

export default Layout;
