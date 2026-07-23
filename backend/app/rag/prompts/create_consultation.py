CREATE_CONSULTATION_PROMPT = """
create_consultation: to book an adoption consultation, follow these
steps in order across the conversation:
1. Get the pet's real id from search_pets — never invent one, and
   re-fetch it right before step 4 rather than reusing an old one.
2. Collect all three of: pet_id, contact, preferred_time, by asking the
   user directly for anything missing. Never invent or use a placeholder
   (e.g. "your email", "example.com", "ASAP") for contact or time.
3. Once all three are known, ask exactly this and then stop and wait —
   do not call the tool yet:
   "Confirm consultation request for [pet name] at [preferred time]? Reply YES to book."
4. Only when the user's very next message is "YES" (case-insensitive),
   call create_consultation with the exact collected values. This tool
   call is required — a sentence claiming it's booked without calling
   the tool is a failure. If the tool returns an error, tell the user
   that error instead of claiming success.
""".strip()
