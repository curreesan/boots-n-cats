import { useState, useEffect, useRef } from "react";
import { useChatSocket } from "../hooks/useChatScoket";
import { useCart } from "../context/useCart";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

function ConsultationPicker({
  petId,
  petName,
  onConfirm,
}: {
  petId: string;
  petName: string;
  onConfirm: (petId: string, petName: string, date: string) => void;
}) {
  const [date, setDate] = useState("");
  const [submitted, setSubmitted] = useState(false);

  if (submitted) {
    return <p className="text-xs text-muted-foreground">Date submitted.</p>;
  }

  return (
    <div className="flex flex-col gap-2">
      <Input
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
        className="h-8 text-xs"
      />
      <Button
        size="sm"
        disabled={!date}
        onClick={() => {
          onConfirm(petId, petName, date);
          setSubmitted(true);
        }}
      >
        Confirm
      </Button>
    </div>
  );
}

function CheckoutConfirm({ onConfirm }: { onConfirm: () => void }) {
  const [submitted, setSubmitted] = useState(false);

  if (submitted) {
    return <p className="text-xs text-muted-foreground">Order submitted.</p>;
  }

  return (
    <Button
      size="sm"
      onClick={() => {
        onConfirm();
        setSubmitted(true);
      }}
    >
      Confirm order
    </Button>
  );
}

function ChatWindow() {
  const { refreshCart } = useCart();
  const { messages, connected, connect, disconnect, sendMessage, confirmConsultation, placeOrder } =
    useChatSocket(refreshCart);
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
            {msg.picker && (
              <div className="mt-2">
                <ConsultationPicker
                  petId={msg.picker.petId}
                  petName={msg.picker.petName}
                  onConfirm={confirmConsultation}
                />
              </div>
            )}
            {msg.checkoutConfirm && (
              <div className="mt-2">
                <CheckoutConfirm onConfirm={placeOrder} />
              </div>
            )}
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
