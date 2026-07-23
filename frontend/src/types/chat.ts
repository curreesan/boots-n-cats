export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  // Present on an assistant message when the backend wants the user to
  // pick a real date instead of typing one — see request_consultation
  // in the backend agent. Rendered as an inline date picker, not text.
  picker?: { petId: string; petName: string };
  // Present on an assistant message when the backend wants the user to
  // explicitly confirm placing their order — see request_checkout in
  // the backend agent. Rendered as an inline "Confirm order" button.
  checkoutConfirm?: { itemCount: number };
};
