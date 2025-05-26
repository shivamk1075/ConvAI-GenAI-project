# import json
# import os
# import ollama
# import shutil
# from datetime import datetime

# # ================================
# # CONFIGURATION
# # ================================
# CONFIG = {
#     'model': 'phi3.5',
#     'max_messages': 50,
#     'temperature': 0.7,
#     'max_tokens': 200,
#     'users_dir': 'users',
#     'templates_dir': 'templates',
#     'backups_dir': 'backups'
# }

# # ================================
# # STORAGE FUNCTIONS
# # ================================
# class SimpleStorage:
#     @staticmethod
#     def ensure_directories():
#         for dir_name in [CONFIG['users_dir'], CONFIG['templates_dir'], CONFIG['backups_dir']]:
#             os.makedirs(dir_name, exist_ok=True)

#     @staticmethod
#     def ensure_user_directory(user_id):
#         user_folder = os.path.join(CONFIG['users_dir'], f'user_{user_id}')
#         os.makedirs(user_folder, exist_ok=True)
#         return user_folder

#     @staticmethod
#     def get_user_file_path(user_id, persona_type):
#         user_folder = SimpleStorage.ensure_user_directory(user_id)
#         return os.path.join(user_folder, f'{persona_type}.json')

#     @staticmethod
#     def save_json(filepath, data):
#         try:
#             os.makedirs(os.path.dirname(filepath), exist_ok=True)
#             with open(filepath, 'w') as f:
#                 json.dump(data, f, indent=2)
#             return True
#         except Exception as e:
#             print(f"Error saving {filepath}: {e}")
#             return False

#     @staticmethod
#     def load_json(filepath):
#         try:
#             if os.path.exists(filepath):
#                 with open(filepath, 'r') as f:
#                     return json.load(f)
#             return None
#         except Exception as e:
#             print(f"Error loading {filepath}: {e}")
#             return None

#     @staticmethod
#     def backup_file(filepath):
#         try:
#             if os.path.exists(filepath):
#                 timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#                 filename = os.path.basename(filepath)
#                 user_folder = os.path.basename(os.path.dirname(filepath))
#                 backup_filename = f"{timestamp}_{user_folder}_{filename}"
#                 backup_path = os.path.join(CONFIG['backups_dir'], backup_filename)
#                 shutil.copy2(filepath, backup_path)
#                 print(f"💾 Backup created: {backup_path}")
#                 return True
#             return False
#         except Exception as e:
#             print(f"Backup failed: {e}")
#             return False

#     @staticmethod
#     def list_users():
#         users = []
#         users_dir = CONFIG['users_dir']
#         if os.path.exists(users_dir):
#             for folder_name in os.listdir(users_dir):
#                 folder_path = os.path.join(users_dir, folder_name)
#                 if os.path.isdir(folder_path) and folder_name.startswith('user_'):
#                     user_id = folder_name[5:]
#                     users.append(user_id)
#         return users

#     @staticmethod
#     def get_user_stats(user_id):
#         stats = {}
#         for persona in ['relative', 'shopkeeper']:
#             filepath = SimpleStorage.get_user_file_path(user_id, persona)
#             conversation = SimpleStorage.load_json(filepath)
#             if conversation:
#                 message_count = len([m for m in conversation.get('messages', []) if m['role'] in ['user', 'assistant']])
#                 stats[persona] = message_count
#             else:
#                 stats[persona] = 0
#         return stats

#     @staticmethod
#     def user_exists(user_id):
#         user_folder = os.path.join(CONFIG['users_dir'], f'user_{user_id}')
#         return os.path.exists(user_folder)

# # ================================
# # PERSONA MANAGER
# # ================================
# class SimplePersonaManager:
#     def __init__(self):
#         SimpleStorage.ensure_directories()
#         self.create_templates()
#         print(f"🤖 AI Trainer initialized (Model: {CONFIG['model']})")

#     def create_templates(self):
#         templates = {
#             'relative': {
#                 "persona_type": "relative",
#                 "description": "Caring cousin who supports business ideas",
#                 "messages": [
#                     {
#                         "role": "system",
#                         "content": "You are a caring cousin who loves hearing about family members' business ideas. Be warm, supportive, and ask thoughtful questions. Keep responses to 1-2 sentences. Never mention being an AI.",
#                         "timestamp": datetime.now().isoformat()
#                     },
#                     {
#                         "role": "assistant",
#                         "content": "Hi there! I'm so excited to hear about your business ideas. What's been on your mind lately?",
#                         "timestamp": datetime.now().isoformat()
#                     }
#                 ]
#             },
#             'shopkeeper': {
#                 "persona_type": "shopkeeper",
#                 "description": "Experienced business advisor",
#                 "messages": [
#                     {
#                         "role": "system",
#                         "content": "You are an experienced shopkeeper who evaluates business opportunities. Focus on practical aspects like profit margins, target customers, competition, and logistics. Ask specific business questions.",
#                         "timestamp": datetime.now().isoformat()
#                     },
#                     {
#                         "role": "assistant",
#                         "content": "Welcome! I've been in retail for 20 years. What business opportunity brings you to me today?",
#                         "timestamp": datetime.now().isoformat()
#                     }
#                 ]
#             }
#         }
#         for persona_type, template in templates.items():
#             template_path = os.path.join(CONFIG['templates_dir'], f"{persona_type}.json")
#             if not os.path.exists(template_path):
#                 SimpleStorage.save_json(template_path, template)
#                 print(f"✅ Created template: {persona_type}")

#     def get_or_create_user_conversation(self, user_id, persona_type):
#         user_file = SimpleStorage.get_user_file_path(user_id, persona_type)
#         conversation = SimpleStorage.load_json(user_file)
#         if conversation:
#             return conversation
#         template_file = os.path.join(CONFIG['templates_dir'], f"{persona_type}.json")
#         template = SimpleStorage.load_json(template_file)
#         if template:
#             conversation = {
#                 "user_id": user_id,
#                 "persona_type": persona_type,
#                 "created_at": datetime.now().isoformat(),
#                 "last_accessed": datetime.now().isoformat(),
#                 "messages": template["messages"].copy()
#             }
#             SimpleStorage.save_json(user_file, conversation)
#             print(f"👤 Created new conversation for {user_id} - {persona_type}")
#             return conversation
#         print(f"❌ Template not found: {persona_type}")
#         return None

#     def save_conversation(self, user_id, persona_type, conversation):
#         user_file = SimpleStorage.get_user_file_path(user_id, persona_type)
#         SimpleStorage.backup_file(user_file)
#         conversation["last_accessed"] = datetime.now().isoformat()
#         return SimpleStorage.save_json(user_file, conversation)

#     def chat(self, user_id, persona_type, user_message):
#         conversation = self.get_or_create_user_conversation(user_id, persona_type)
#         if not conversation:
#             return "Error: Could not load conversation"
#         conversation["messages"].append({
#             "role": "user",
#             "content": user_message,
#             "timestamp": datetime.now().isoformat()
#         })
#         try:
#             messages_for_ai = conversation["messages"][-10:]
#             response = ollama.chat(
#                 model=CONFIG['model'],
#                 messages=messages_for_ai,
#                 options={
#                     'temperature': CONFIG['temperature'],
#                     'max_tokens': CONFIG['max_tokens']
#                 }
#             )
#             ai_response = response['message']['content'].strip()
#             conversation["messages"].append({
#                 "role": "assistant",
#                 "content": ai_response,
#                 "timestamp": datetime.now().isoformat()
#             })
#             self.save_conversation(user_id, persona_type, conversation)
#             return ai_response
#         except Exception as e:
#             error_msg = f"AI Error: {e}"
#             print(f"❌ {error_msg}")
#             return error_msg

# # ================================
# # USER MANAGEMENT
# # ================================
# def show_user_menu():
#     users = SimpleStorage.list_users()
#     if users:
#         print(f"\n👥 Existing users: {', '.join(users)}")
#         print("📝 Or enter a new user ID to create new user")
#     else:
#         print("\n👤 No existing users found")
#         print("📝 Enter a user ID to create your first user")
#     user_id = input("\n🆔 Enter user ID: ").strip()
#     if SimpleStorage.user_exists(user_id):
#         stats = SimpleStorage.get_user_stats(user_id)
#         print(f"\n📊 User stats - Relative: {stats['relative']} messages, Shopkeeper: {stats['shopkeeper']} messages")
#     else:
#         print(f"\n👤 Creating new user folder: user_{user_id}")
#     return user_id

# # ================================
# # SESSION HANDLERS
# # ================================
# def start_relative_session():
#     print("\n" + "="*50)
#     print("🤗 RELATIVE TRAINING SESSION")
#     print("="*50)
#     user_id = show_user_menu()
#     conversation = manager.get_or_create_user_conversation(user_id, 'relative')
#     for msg in reversed(conversation["messages"]):
#         if msg["role"] == "assistant":
#             print(f"\n🤗 Relative: {msg['content']}")
#             break
#     start_chat_loop(user_id, 'relative', '🤗 Relative')

# def start_shopkeeper_session():
#     print("\n" + "="*50)
#     print("🏪 SHOPKEEPER TRAINING SESSION")
#     print("="*50)
#     user_id = show_user_menu()
#     conversation = manager.get_or_create_user_conversation(user_id, 'shopkeeper')
#     for msg in reversed(conversation["messages"]):
#         if msg["role"] == "assistant":
#             print(f"\n🏪 Shopkeeper: {msg['content']}")
#             break
#     start_chat_loop(user_id, 'shopkeeper', '🏪 Shopkeeper')

# def start_chat_loop(user_id, persona_type, display_name):
#     max_messages = CONFIG['max_messages']
#     message_count = 0
#     print(f"\n💬 Chat Session (Max {max_messages} messages)")
#     print("Commands: 'exit' to end | 'stats' for statistics | 'backup' to create backup")
#     print("-" * 60)
#     while message_count < max_messages:
#         try:
#             user_input = input(f"\n👤 You: ").strip()
#             if not user_input:
#                 continue
#             if user_input.lower() in ['exit', 'quit', 'bye']:
#                 print("👋 Ending session...")
#                 break
#             elif user_input.lower() == 'stats':
#                 stats = SimpleStorage.get_user_stats(user_id)
#                 print(f"\n📊 Your conversation stats:")
#                 print(f"   🤗 Relative: {stats['relative']} messages")
#                 print(f"   🏪 Shopkeeper: {stats['shopkeeper']} messages")
#                 continue
#             elif user_input.lower() == 'backup':
#                 user_file = SimpleStorage.get_user_file_path(user_id, persona_type)
#                 SimpleStorage.backup_file(user_file)
#                 continue
#             message_count += 1
#             print("🤖 Thinking...")
#             ai_response = manager.chat(user_id, persona_type, user_input)
#             print(f"\n{display_name}: {ai_response}")
#             remaining = max_messages - message_count
#             if remaining > 0:
#                 print(f"\n📊 Messages remaining: {remaining}")
#             else:
#                 print("\n🎯 Training session completed!")
#                 break
#         except KeyboardInterrupt:
#             print("\n\n⚠️ Session interrupted")
#             break
#         except Exception as e:
#             print(f"❌ Unexpected error: {e}")
#             break
#     print(f"\n{'='*60}")
#     print(f"📋 SESSION SUMMARY")
#     print(f"{'='*60}")
#     print(f"👤 User: {user_id}")
#     print(f"🎭 Persona: {display_name}")
#     print(f"💬 Messages this session: {message_count}")
#     stats = SimpleStorage.get_user_stats(user_id)
#     total_messages = stats['relative'] + stats['shopkeeper']
#     print(f"📊 Total messages across all personas: {total_messages}")
#     print(f"💾 All conversations saved automatically ✅")
#     print(f"{'='*60}")

# # ================================
# # GLOBAL MANAGER
# # ================================
# manager = SimplePersonaManager()



# import os
# import json
# import ollama
# from datetime import datetime

# USERS_DIR = 'users'

# def ensure_user_folder(user_id):
#     folder = os.path.join(USERS_DIR, f'user_{user_id}')
#     os.makedirs(folder, exist_ok=True)
#     return folder

# def get_conversation_path(user_id, persona_type):
#     folder = ensure_user_folder(user_id)
#     return os.path.join(folder, f'{persona_type}.json')

# def load_conversation(user_id, persona_type):
#     path = get_conversation_path(user_id, persona_type)
#     if os.path.exists(path):
#         with open(path, 'r') as f:
#             return json.load(f)
#     # Start a new conversation if none exists
#     return {
#         "user_id": user_id,
#         "persona": persona_type,
#         "created_at": datetime.now().isoformat(),
#         "messages": []
#     }

# def save_conversation(user_id, persona_type, conversation):
#     path = get_conversation_path(user_id, persona_type)
#     with open(path, 'w') as f:
#         json.dump(conversation, f, indent=2)

# def chat(user_id, persona_type, user_message):
#     conversation = load_conversation(user_id, persona_type)
#     conversation["messages"].append({
#         "role": "user",
#         "content": user_message,
#         "timestamp": datetime.now().isoformat()
#     })
#     try:
#         # Use last 10 messages for context
#         messages_for_ai = conversation["messages"][-1:]
#         response = ollama.chat(
#             model='phi3.5',
#             messages=messages_for_ai
#         )
#         ai_response = response['message']['content'].strip()
#         conversation["messages"].append({
#             "role": "assistant",
#             "content": ai_response,
#             "timestamp": datetime.now().isoformat()
#         })
#         save_conversation(user_id, persona_type, conversation)
#         return ai_response
#     except Exception as e:
#         return f"AI Error: {e}"

# def list_users():
#     if not os.path.exists(USERS_DIR):
#         return []
#     return [d[5:] for d in os.listdir(USERS_DIR) if d.startswith('user_') and os.path.isdir(os.path.join(USERS_DIR, d))]

# def show_user_menu():
#     users = list_users()
#     if users:
#         print(f"\n👥 Existing users: {', '.join(users)}")
#     user_id = input("\n🆔 Enter user ID: ").strip()
#     return user_id

# def start_session(persona_type, display_name):
#     print(f"\n{'='*50}\n{display_name.upper()} SESSION\n{'='*50}")
#     user_id = show_user_menu()
#     conversation = load_conversation(user_id, persona_type)
#     # Show last AI message if exists
#     for msg in reversed(conversation["messages"]):
#         if msg["role"] == "assistant":
#             print(f"\n{display_name}: {msg['content']}")
#             break
#     max_messages = 50
#     message_count = 0
#     print(f"\n💬 Chat Session (Max {max_messages} messages)")
#     print("Type 'exit' to end session")
#     print("-" * 40)
#     while message_count < max_messages:
#         user_input = input(f"\n👤 You: ").strip()
#         if not user_input or user_input.lower() in ['exit', 'quit', 'bye']:
#             break
#         message_count += 1
#         print("🤖 Thinking...")
#         ai_response = chat(user_id, persona_type, user_input)
#         print(f"\n{display_name}: {ai_response}")
#         remaining = max_messages - message_count
#         if remaining > 0:
#             print(f"\n📊 Messages remaining: {remaining}")
#     print(f"\n✅ Session completed! Conversation saved for user: {user_id}")

# def start_relative_session():
#     start_session('relative', 'Relative')

# def start_shopkeeper_session():
#     start_session('shopkeeper', 'Shopkeeper')


# Implemented template conversation history into new user's own persona 

import json
import ollama
from datetime import datetime
import os

USERS_DIR = 'users'
TEMPLATES_DIR = 'templates'

def ensure_user_folder(user_id):
    folder = os.path.join(USERS_DIR, f'user_{user_id}')
    os.makedirs(folder, exist_ok=True)
    return folder

def get_conversation_path(user_id, persona_type):
    folder = ensure_user_folder(user_id)
    return os.path.join(folder, f'{persona_type}.json')

def get_template_path(persona_type):
    return os.path.join(TEMPLATES_DIR, f'{persona_type}.json')

def load_conversation(user_id, persona_type):
    path = get_conversation_path(user_id, persona_type)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    # If not exists, copy from template
    template_path = get_template_path(persona_type)
    if os.path.exists(template_path):
        with open(template_path, 'r') as f:
            template = json.load(f)
        # Add user and timestamp info to the new conversation
        return {
            "user_id": user_id,
            "persona": persona_type,
            "created_at": datetime.now().isoformat(),
            "messages": template.get("messages", [])
        }
    # Fallback to empty conversation if no template found
    return {
        "user_id": user_id,
        "persona": persona_type,
        "created_at": datetime.now().isoformat(),
        "messages": []
    }

def save_conversation(user_id, persona_type, conversation):
    path = get_conversation_path(user_id, persona_type)
    with open(path, 'w') as f:
        json.dump(conversation, f, indent=2)

def chat(user_id, persona_type, user_message):
    conversation = load_conversation(user_id, persona_type)
    conversation["messages"].append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().isoformat()
    })
    try:
        # Use last 10 messages for context
        messages_for_ai = conversation["messages"][-10:]
        response = ollama.chat(
            model='phi3.5',
            messages=messages_for_ai
        )
        ai_response = response['message']['content'].strip()
        conversation["messages"].append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        save_conversation(user_id, persona_type, conversation)
        return ai_response
    except Exception as e:
        return f"AI Error: {e}"

def list_users():
    if not os.path.exists(USERS_DIR):
        return []
    return [d[5:] for d in os.listdir(USERS_DIR) if d.startswith('user_') and os.path.isdir(os.path.join(USERS_DIR, d))]

def show_user_menu():
    users = list_users()
    if users:
        print(f"\n👥 Existing users: {', '.join(users)}")
    user_id = input("\n🆔 Enter user ID: ").strip()
    return user_id

def start_session(persona_type, display_name):
    print(f"\n{'='*50}\n{display_name.upper()} SESSION\n{'='*50}")
    user_id = show_user_menu()
    conversation = load_conversation(user_id, persona_type)
    # Show last AI message if exists
    for msg in reversed(conversation["messages"]):
        if msg["role"] == "assistant":
            print(f"\n{display_name}: {msg['content']}")
            break
    max_messages = 50
    message_count = 0
    print(f"\n💬 Chat Session (Max {max_messages} messages)")
    print("Type 'exit' to end session")
    print("-" * 40)
    while message_count < max_messages:
        user_input = input(f"\n👤 You: ").strip()
        if not user_input or user_input.lower() in ['exit', 'quit', 'bye']:
            break
        message_count += 1
        print("🤖 Thinking...")
        ai_response = chat(user_id, persona_type, user_input)
        print(f"\n{display_name}: {ai_response}")
        remaining = max_messages - message_count
        if remaining > 0:
            print(f"\n📊 Messages remaining: {remaining}")
    print(f"\n✅ Session completed! Conversation saved for user: {user_id}")

def start_relative_session():
    start_session('relative', 'Relative')

def start_shopkeeper_session():
    start_session('shopkeeper', 'Shopkeeper')
