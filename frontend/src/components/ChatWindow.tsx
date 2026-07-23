import { useState, useEffect, useRef } from "react";
import { useChatSocket } from "../hooks/useChatScoket";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

function ChatWindow() {
  const { messages, connected, connect, disconnect, sendMessage } =
    useChatSocket();
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    connect();
    return () => disconnect();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function handleSend(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;
    sendMessage(input);
    setInput("");
  }

  return (
    <div className="flex h-[28rem] w-80 flex-col overflow-hidden rounded-xl border border-border bg-card shadow-lg sm:w-96">
      <div className="border-b border-border px-4 py-3 text-sm font-semibold">
        Boots n&apos; Cats Assistant
      </div>

      <div className="flex flex-1 flex-col gap-2 overflow-y-auto p-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={cn(
              "max-w-[85%] rounded-lg px-3 py-2 text-sm",
              msg.role === "user"
                ? "self-end bg-primary text-primary-foreground"
                : "self-start bg-muted text-foreground",
            )}
          >
            {msg.content}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <form className="flex gap-2 border-t border-border p-2" onSubmit={handleSend}>
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={connected ? "Type a message..." : "Connecting..."}
          disabled={!connected}
        />
        <Button type="submit" size="sm" disabled={!connected}>
          Send
        </Button>
      </form>
    </div>
  );
}

export default ChatWindow;
