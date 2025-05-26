import json
import os
import shutil
from datetime import datetime
import ollama

class BackendTester:
    def __init__(self):
        self.templates_dir = 'templates'
        self.users_dir = 'users'
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.users_dir, exist_ok=True)
        print("🚀 AI Training Platform Backend Tester")
        print("=" * 50)
    
    def create_standard_templates(self):
        """Step 1: Create standard persona templates"""
        print("\n📁 Step 1: Creating Standard Templates")
        
        # Relative Template
        relative_template = {
            "persona_type": "relative",
            "template_version": "1.0",
            "created_at": datetime.now().isoformat(),
            "description": "Caring cousin persona",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a caring cousin who loves hearing about family members' business ideas. Be warm, supportive, and ask thoughtful questions. Keep responses to 1-2 sentences. Never mention being an AI."
                },
                {
                    "role": "assistant",
                    "content": "Hi there! I'm so excited to hear about your business ideas. What's been on your mind lately?"
                },
                {
                    "role": "user",
                    "content": "I've been thinking about starting my own business."
                },
                {
                    "role": "assistant",
                    "content": "That's wonderful! I'm so proud of you for taking this step. What kind of business are you thinking about?"
                }
            ]
        }
        
        # Shopkeeper Template
        shopkeeper_template = {
            "persona_type": "shopkeeper",
            "template_version": "1.0",
            "created_at": datetime.now().isoformat(),
            "description": "Experienced business shopkeeper",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an experienced shopkeeper who evaluates business opportunities. Focus on practical aspects like profit margins, target customers, competition, and logistics. Ask specific business questions."
                },
                {
                    "role": "assistant",
                    "content": "Welcome! I've been in retail for 20 years. What business opportunity brings you to me today?"
                },
                {
                    "role": "user",
                    "content": "I want to start a business and need advice."
                },
                {
                    "role": "assistant",
                    "content": "Smart to get advice first. What type of business and what's your target market?"
                }
            ]
        }
        
        # Save templates
        with open(f'{self.templates_dir}/standard_relative.json', 'w') as f:
            json.dump(relative_template, f, indent=2)
        
        with open(f'{self.templates_dir}/standard_shopkeeper.json', 'w') as f:
            json.dump(shopkeeper_template, f, indent=2)
        
        print("✅ Created: templates/standard_relative.json")
        print("✅ Created: templates/standard_shopkeeper.json")
        
        # Show file structure
        self.show_file_structure()
    
    def create_user(self, user_id):
        """Step 2: Create user with copied personas"""
        print(f"\n👤 Step 2: Creating User {user_id}")
        
        # Create user folder
        user_folder = f'{self.users_dir}/user_{user_id}'
        os.makedirs(user_folder, exist_ok=True)
        print(f"✅ Created folder: {user_folder}")
        
        # Load templates
        with open(f'{self.templates_dir}/standard_relative.json', 'r') as f:
            relative_template = json.load(f)
        
        with open(f'{self.templates_dir}/standard_shopkeeper.json', 'r') as f:
            shopkeeper_template = json.load(f)
        
        # Create user-specific persona files
        user_relative = {
            "user_id": user_id,
            "persona_type": "relative",
            "created_from_template": "standard_relative",
            "created_at": datetime.now().isoformat(),
            "messages": relative_template['messages'].copy()
        }
        
        user_shopkeeper = {
            "user_id": user_id,
            "persona_type": "shopkeeper", 
            "created_from_template": "standard_shopkeeper",
            "created_at": datetime.now().isoformat(),
            "messages": shopkeeper_template['messages'].copy()
        }
        
        # Save user personas
        with open(f'{user_folder}/relative_{user_id}.json', 'w') as f:
            json.dump(user_relative, f, indent=2)
        
        with open(f'{user_folder}/shopkeeper_{user_id}.json', 'w') as f:
            json.dump(user_shopkeeper, f, indent=2)
        
        print(f"✅ Created: {user_folder}/relative_{user_id}.json")
        print(f"✅ Created: {user_folder}/shopkeeper_{user_id}.json")
        
        # Show file structure
        self.show_file_structure()
    
    def chat_with_persona(self, user_id, persona_type, user_message):
        """Step 3: Test chat functionality"""
        print(f"\n💬 Step 3: Chat Test - User {user_id} with {persona_type}")
        
        # Load user's persona file
        user_folder = f'{self.users_dir}/user_{user_id}'
        persona_file = f'{user_folder}/{persona_type}_{user_id}.json'
        
        if not os.path.exists(persona_file):
            print(f"❌ Error: {persona_file} not found")
            return
        
        # Load conversation
        with open(persona_file, 'r') as f:
            conversation = json.load(f)
        
        print(f"📖 Current conversation length: {len(conversation['messages'])} messages")
        
        # Add user message
        conversation['messages'].append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"👤 User: {user_message}")
        
        # Get last 6 messages for context
        messages_for_ai = conversation['messages'][-6:]
        
        try:
            # Get AI response
            print("🤖 Getting AI response...")
            response = ollama.chat(model='phi3.5', messages=messages_for_ai)
            ai_response = response['message']['content'].strip()
            
            # Add AI response
            conversation['messages'].append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Save updated conversation
            with open(persona_file, 'w') as f:
                json.dump(conversation, f, indent=2)
            
            print(f"🤖 {persona_type.title()}: {ai_response}")
            print(f"💾 Conversation saved to {persona_file}")
            print(f"📊 New conversation length: {len(conversation['messages'])} messages")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    def show_file_structure(self):
        """Display current file structure"""
        print("\n📂 Current File Structure:")
        print("ai_training_platform/")
        
        # Show templates
        if os.path.exists(self.templates_dir):
            print("├── templates/")
            for file in os.listdir(self.templates_dir):
                if file.endswith('.json'):
                    print(f"│   ├── {file}")
        
        # Show users
        if os.path.exists(self.users_dir):
            print("├── users/")
            for user_folder in os.listdir(self.users_dir):
                user_path = os.path.join(self.users_dir, user_folder)
                if os.path.isdir(user_path):
                    print(f"│   ├── {user_folder}/")
                    for file in os.listdir(user_path):
                        if file.endswith('.json'):
                            print(f"│   │   ├── {file}")
        print()
    
    def show_conversation_content(self, user_id, persona_type):
        """Display conversation content"""
        print(f"\n📄 Conversation Content: User {user_id} - {persona_type}")
        
        persona_file = f'{self.users_dir}/user_{user_id}/{persona_type}_{user_id}.json'
        
        if os.path.exists(persona_file):
            with open(persona_file, 'r') as f:
                conversation = json.load(f)
            
            print("=" * 60)
            for i, msg in enumerate(conversation['messages']):
                if msg['role'] != 'system':  # Skip system messages for readability
                    role = "🤖 AI" if msg['role'] == 'assistant' else "👤 User"
                    print(f"{role}: {msg['content']}")
                    print("-" * 40)
            print("=" * 60)
        else:
            print(f"❌ File not found: {persona_file}")
    
    def test_multiple_users(self):
        """Test multiple users scenario"""
        print("\n🔄 Step 4: Testing Multiple Users")
        
        users = ['alice', 'bob', 'charlie']
        
        for user in users:
            print(f"\n--- Creating user: {user} ---")
            self.create_user(user)
        
        print("\n📊 Multiple Users File Structure:")
        self.show_file_structure()

def main():
    """Main testing function"""
    tester = BackendTester()
    
    while True:
        print("\n" + "="*50)
        print("🎮 BACKEND TESTING MENU")
        print("="*50)
        print("1. Create Standard Templates")
        print("2. Create User")
        print("3. Chat with Persona")
        print("4. Show File Structure") 
        print("5. Show Conversation Content")
        print("6. Test Multiple Users")
        print("7. Exit")
        
        choice = input("\n🎯 Choose option (1-7): ").strip()
        
        if choice == '1':
            tester.create_standard_templates()
            
        elif choice == '2':
            user_id = input("Enter user ID: ").strip()
            if user_id:
                tester.create_user(user_id)
            else:
                print("❌ Invalid user ID")
                
        elif choice == '3':
            user_id = input("Enter user ID: ").strip()
            persona = input("Enter persona (relative/shopkeeper): ").strip().lower()
            message = input("Enter your message: ").strip()
            
            if user_id and persona in ['relative', 'shopkeeper'] and message:
                tester.chat_with_persona(user_id, persona, message)
            else:
                print("❌ Invalid input")
                
        elif choice == '4':
            tester.show_file_structure()
            
        elif choice == '5':
            user_id = input("Enter user ID: ").strip()
            persona = input("Enter persona (relative/shopkeeper): ").strip().lower()
            
            if user_id and persona in ['relative', 'shopkeeper']:
                tester.show_conversation_content(user_id, persona)
            else:
                print("❌ Invalid input")
                
        elif choice == '6':
            tester.test_multiple_users()
            
        elif choice == '7':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
