import { useState } from "react";
import { useAuth } from "../context/useAuth";
import ChatWindow from "./ChatWindow";
import "../styles/ChatWidget.css";

function ChatWidget() {
  const { user } = useAuth();
  const [open, setOpen] = useState(false);

  if (!user) return null;

  return (
    <div className="chat-widget">
      {open && <ChatWindow />}
      <button className="chat-widget__toggle" onClick={() => setOpen(!open)}>
        {open ? "Close" : "Chat"}
      </button>
    </div>
  );
}

export default ChatWidget;
