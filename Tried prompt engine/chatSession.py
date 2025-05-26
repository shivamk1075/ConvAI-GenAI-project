# # chat_session.py

# from storage import (
#     load_user_state,
#     save_summary,
#     append_to_cache,
#     clear_cache,
#     get_recent_history,
# )
# from ollama_api import ollama_chat   # your wrapper around the Ollama CLI/SDK

# class ChatSession:
#     """
#     Manages a persona-driven chat session with rolling summarization
#     and persistent memory per user.
#     """

#     def __init__(
#         self,
#         user_id: str,
#         persona_preamble: str,
#         summary_block_size: int = 10,
#         model: str = "phi3.5",
#     ):
#         self.user_id = user_id
#         self.persona_preamble = persona_preamble
#         self.summary_block_size = summary_block_size
#         self.model = model

#         # Load any existing rolling summary (long‐term memory)
#         # We ignore the returned recent_history here, since we'll fetch it
#         # on demand from Redis.
#         self.summary_ctx, _ = load_user_state(self.user_id)

#     def run(self):
#         """
#         Start the REPL loop. Type 'exit' or 'quit' to end the session.
#         """
#         print(f"\n[Session started for user: {self.user_id}]")
#         print("Type 'exit' or 'quit' to end.\n")

#         while True:
#             user_msg = input("You: ").strip()
#             if user_msg.lower() in ("exit", "quit"):
#                 print("\n👋 Session ended. Goodbye!\n")
#                 break

#             reply = self.handle_message(user_msg)
#             print(f"\nAI: {reply}\n")

#     def handle_message(self, user_msg: str) -> str:
#         """
#         1. Cache the user turn
#         2. Build the prompt (persona + summary + recent history + new user message)
#         3. Call Ollama
#         4. Cache the assistant turn
#         5. Possibly roll up a summary block
#         """
#         # 1. Cache user turn
#         append_to_cache(self.user_id, "user", user_msg)

#         # 2. Build messages
#         messages = [
#             {"role": "system", "content": self.persona_preamble}
#         ]
#         if self.summary_ctx:
#             messages.append(
#                 {"role": "system", "content": f"Summary so far: {self.summary_ctx}"}
#             )

#         # Fetch the last N turns from Redis
#         recent_turns = get_recent_history(self.user_id)
#         for role, text in recent_turns:
#             messages.append({"role": role, "content": text})

#         # 3. Call the model
#         assistant_reply = ollama_chat(model=self.model, messages=messages)

#         # 4. Cache assistant turn
#         append_to_cache(self.user_id, "assistant", assistant_reply)

#         # 5. Roll up summary if needed
#         self._maybe_summarize()

#         return assistant_reply

#     def _maybe_summarize(self):
#         """
#         If we've hit the summary_block_size in cached turns,
#         summarize them, merge into the rolling summary, persist, and clear cache.
#         """
#         recent_turns = get_recent_history(self.user_id)
#         if len(recent_turns) >= self.summary_block_size:
#             rollup = self._summarize_block(recent_turns)

#             # Merge with existing summary
#             if self.summary_ctx:
#                 self.summary_ctx = (self.summary_ctx + " " + rollup).strip()
#             else:
#                 self.summary_ctx = rollup

#             # Persist to SQLite
#             save_summary(self.user_id, self.summary_ctx)

#             # Clear Redis cache for this user
#             clear_cache(self.user_id)

#     def _summarize_block(self, block_turns) -> str:
#         """
#         Use the same LLM to create a 1–2 line summary of a block of turns.
#         """
#         convo_text = "\n".join(f"{role}: {text}" for role, text in block_turns)
#         prompt = [
#             {
#                 "role": "system",
#                 "content": "You are a concise summarizer. In 2 lines max, summarize the following conversation:"
#             },
#             {"role": "user", "content": convo_text}
#         ]
#         summary = ollama_chat(model=self.model, messages=prompt)
#         return summary.strip()


# Added the first turn feature:# chat_session.py

from storage import (
    load_user_state,
    save_summary,
    append_to_cache,
    clear_cache,
    get_recent_history,
)
from ollama_api import ollama_chat

class ChatSession:
    """
    Manages a persona‐driven chat session with:
    - a one‐time summary injection if it exists
    - rolling short‐term history
    - periodic block summarization
    """

    def __init__(
        self,
        user_id: str,
        persona_preamble: str,
        summary_block_size: int = 10,
        model: str = "phi3.5",
    ):
        self.user_id = user_id
        self.persona_preamble = persona_preamble
        self.summary_block_size = summary_block_size
        self.model = model

        # Load long‐term summary (ignore recent history here)
        self.summary_ctx, _ = load_user_state(self.user_id)

        # Flag to indicate we haven't yet sent the first turn
        self._first_turn = True

    def run(self):
        print(f"\n[Session started for user: {self.user_id}]")
        print("Type 'exit' or 'quit' to end.\n")

        while True:
            user_msg = input("You: ").strip()
            if user_msg.lower() in ("exit", "quit"):
                print("\n👋 Session ended. Goodbye!\n")
                break

            reply = self.handle_message(user_msg)
            print(f"\nAI: {reply}\n")

    def handle_message(self, user_msg: str) -> str:
        # 1) Cache the user turn
        append_to_cache(self.user_id, "user", user_msg)

        # 2) Build the prompt
        messages = self._build_prompt(user_msg)

        # 3) Call the model
        assistant_reply = ollama_chat(model=self.model, messages=messages)

        # 4) Cache assistant turn
        append_to_cache(self.user_id, "assistant", assistant_reply)

        # 5) Maybe roll up a summary block
        self._maybe_summarize()

        return assistant_reply

    def _build_prompt(self, user_msg: str):
        """
        Construct the messages list:
        - Always the persona preamble
        - On first turn: inject summary_ctx (if any)
        - On subsequent turns: inject the last N cached turns
        - Finally, the new user message
        """
        msgs = [{"role": "system", "content": self.persona_preamble}]

        if self._first_turn:
            # One‐time summary injection
            if self.summary_ctx:
                msgs.append(
                    {"role": "system", "content": f"Summary so far: {self.summary_ctx}"}
                )
            self._first_turn = False

        # else:
        #     # On subsequent turns, replay the recent N turns
        #     for role, text in get_recent_history(self.user_id):
        #         msgs.append({"role": role, "content": text})

        # Always append the incoming user message last
        msgs.append({"role": "user", "content": user_msg})
        return msgs

    def _maybe_summarize(self):
        recent = get_recent_history(self.user_id)
        if len(recent) >= self.summary_block_size:
            rollup = self._summarize_block(recent)

            # Merge into the long-term summary
            if self.summary_ctx:
                self.summary_ctx = (self.summary_ctx + " " + rollup).strip()
            else:
                self.summary_ctx = rollup

            save_summary(self.user_id, self.summary_ctx)
            clear_cache(self.user_id)

    def _summarize_block(self, block_turns) -> str:
        convo = "\n".join(f"{role}: {text}" for role, text in block_turns)
        prompt = [
            {"role": "system",
             "content": "You are a concise summarizer. In 2 lines max, summarize:"},
            {"role": "user", "content": convo}
        ]
        return ollama_chat(model=self.model, messages=prompt).strip()
