# personas.py

from chatSession import ChatSession

def start_relative_session():
    """
    Launch a chat session with the “relative” persona.
    """
    print("\n🧑‍🤝‍🧑 Starting AI Trainer as your personal relative…")
    user_id = input("Enter your user ID (e.g. your name or email): ").strip()
    if not user_id:
        user_id = "default_relative"

    persona_preamble = (
        "You are a caring personal relative. "
        "You speak warmly, offer empathy, and give advice as a trusted family member.Answer only in 25 words or less."
    )

    session = ChatSession(
        user_id=user_id,
        persona_preamble=persona_preamble,
        summary_block_size=10  # number of turns before auto-summarizing
    )
    session.run()


def start_shopkeeper_session():
    """
    Launch a chat session with the “shopkeeper” persona.
    """
    print("\n🏪 Starting AI Trainer as a friendly shopkeeper…")
    user_id = input("Enter your user ID (e.g. your name or email): ").strip()
    if not user_id:
        user_id = "default_shopkeeper"

    persona_preamble = (
        "You are an experienced shopkeeper. "
        "You greet customers politely, share product knowledge, "
        "recommend items, and handle objections with patience. Answer only in 25 words or less."
    )

    session = ChatSession(
        user_id=user_id,
        persona_preamble=persona_preamble,
        summary_block_size=10  # number of turns before auto-summarizing
    )
    session.run()
