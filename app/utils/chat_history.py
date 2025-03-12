from typing import Dict, List, Optional

# Global dictionary to store message history for each chat
chat_history_storage: Dict[int, List[Dict[str, str]]] = {}
HISTORY_LIMIT = 10


def store_message_in_history(chat_id: int, message_text: Optional[str], role: str = "user") -> None:
    if not message_text:
        return

    message = {"role": role, "content": message_text}

    if chat_id not in chat_history_storage:
        chat_history_storage[chat_id] = []

    # Add the message to history
    chat_history_storage[chat_id].append(message)

    # Keep only the last LIMIT messages to avoid memory issues
    if len(chat_history_storage[chat_id]) > HISTORY_LIMIT:
        chat_history_storage[chat_id] = chat_history_storage[chat_id][-HISTORY_LIMIT:]


def get_chat_history(chat_id: int, limit: int = HISTORY_LIMIT) -> List[str]:
    if chat_id not in chat_history_storage:
        return []

    return chat_history_storage[chat_id][-limit:]
