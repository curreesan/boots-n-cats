import { useState } from "react";
import { MessageCircle, X } from "lucide-react";
import { useAuth } from "../context/useAuth";
import { Button } from "@/components/ui/button";
import ChatWindow from "./ChatWindow";

function ChatWidget() {
  const { user } = useAuth();
  const [open, setOpen] = useState(false);

  if (!user) return null;

  return (
    <div className="fixed right-6 bottom-6 z-20 flex flex-col items-end gap-3">
      {open && <ChatWindow />}
      <Button
        size="icon"
        className="size-14 rounded-full shadow-lg"
        onClick={() => setOpen(!open)}
        aria-label={open ? "Close chat" : "Open chat"}
      >
        {open ? (
          <X className="size-6" />
        ) : (
          <MessageCircle className="size-6" />
        )}
      </Button>
    </div>
  );
}

export default ChatWidget;
