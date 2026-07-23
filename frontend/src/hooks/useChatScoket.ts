import { useState, useRef, useCallback } from "react";
import type { ChatMessage } from "../types/chat";
import { WS_BASE_URL } from "../api/config";

export function useChatSocket() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [connected, setConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    if (socketRef.current) return;

    const socket = new WebSocket(`${WS_BASE_URL}/ws/chat`);
    socketRef.current = socket;

    socket.onopen = () => {
      if (socketRef.current === socket) setConnected(true);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
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

  return { messages, connected, connect, disconnect, sendMessage };
}
