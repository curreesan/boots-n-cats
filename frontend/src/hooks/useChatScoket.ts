import { useState, useRef, useCallback, useEffect } from "react";
import type { ChatMessage } from "../types/chat";
import { WS_BASE_URL } from "../api/config";

export function useChatSocket(onCartUpdated?: () => void) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [connected, setConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  // A ref, not a dependency of `connect`, so a new onCartUpdated identity
  // on every render doesn't force the socket to reconnect — the socket
  // handler below always reads the latest callback via this ref instead.
  const onCartUpdatedRef = useRef(onCartUpdated);
  useEffect(() => {
    onCartUpdatedRef.current = onCartUpdated;
  }, [onCartUpdated]);

  const connect = useCallback(() => {
    if (socketRef.current) return;

    const socket = new WebSocket(`${WS_BASE_URL}/ws/chat`);
    socketRef.current = socket;

    socket.onopen = () => {
      if (socketRef.current === socket) setConnected(true);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "consultation_picker") {
        setMessages((current) => [
          ...current,
          {
            role: "assistant",
            content: `When would you like a callback about ${data.pet_name}?`,
            picker: { petId: data.pet_id, petName: data.pet_name },
          },
        ]);
        return;
      }
      if (data.type === "checkout_confirm") {
        setMessages((current) => [
          ...current,
          {
            role: "assistant",
            content: `Ready to place your order (${data.item_count} item${data.item_count === 1 ? "" : "s"})?`,
            checkoutConfirm: { itemCount: data.item_count },
          },
        ]);
        return;
      }
      if (data.cart_updated) {
        onCartUpdatedRef.current?.();
      }
      setMessages((current) => [
        ...current,
        { role: "assistant", content: data.content },
      ]);
    };

    socket.onclose = () => {
      if (socketRef.current === socket) {
        setConnected(false);
        socketRef.current = null;
      }
    };
  }, []);

  const disconnect = useCallback(() => {
    socketRef.current?.close();
    socketRef.current = null;
  }, []);

  const sendMessage = useCallback((content: string) => {
    if (!socketRef.current) return;
    setMessages((current) => [...current, { role: "user", content }]);
    socketRef.current.send(JSON.stringify({ content }));
  }, []);

  const confirmConsultation = useCallback((petId: string, petName: string, preferredDate: string) => {
    if (!socketRef.current) return;
    setMessages((current) => [
      ...current,
      { role: "user", content: `Preferred date for ${petName}: ${preferredDate}` },
    ]);
    socketRef.current.send(
      JSON.stringify({ type: "consultation_confirm", pet_id: petId, preferred_date: preferredDate }),
    );
  }, []);

  const placeOrder = useCallback(() => {
    if (!socketRef.current) return;
    setMessages((current) => [...current, { role: "user", content: "Confirm order" }]);
    socketRef.current.send(JSON.stringify({ type: "checkout_place" }));
  }, []);

  return { messages, connected, connect, disconnect, sendMessage, confirmConsultation, placeOrder };
}
