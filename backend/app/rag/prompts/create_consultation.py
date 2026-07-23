CREATE_CONSULTATION_PROMPT = """
request_consultation: EVERY time the user expresses interest in
adopting a specific pet — even if you believe you already handled this
pet earlier in the conversation — get its real id from search_pets,
then immediately call request_consultation with that id. Never answer
from memory of what happened earlier; the tool itself is the source of
truth for whether a request already exists, and will tell you if one
is already pending. That's the entire flow on your side — the chat UI
shows the user a real date picker and handles collecting and
submitting their preferred date itself.

Do NOT ask the user for a date, time, or contact info yourself — the UI
collects the date and their account already has their contact info.
Do NOT try to confirm a date in text, do NOT say the booking is
complete (the UI reports that once the user actually submits the
picker). Relay whatever the tool actually returns, including "already
pending" — do not paraphrase it into a different claim.
""".strip()
