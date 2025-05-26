class UserManager:
    def __init__(self, users_dir='users', templates_dir='templates'):
        self.users_dir = users_dir
        self.templates_dir = templates_dir
        self.template_manager = TemplateManager(templates_dir)
        os.makedirs(self.users_dir, exist_ok=True)
    
    def create_user(self, user_id):
        """Create new user with persona copies"""
        user_folder = os.path.join(self.users_dir, f'user_{user_id}')
        os.makedirs(user_folder, exist_ok=True)
        
        # Copy templates to user's folder
        self.initialize_user_personas(user_id)
        
        return user_folder
    
    def initialize_user_personas(self, user_id):
        """Create user-specific persona files from templates"""
        
        # Get templates
        relative_template = self.template_manager.get_template('relative')
        shopkeeper_template = self.template_manager.get_template('shopkeeper')
        
        if relative_template and shopkeeper_template:
            # Create user-specific versions
            user_relative = {
                "user_id": user_id,
                "persona_type": "relative", 
                "created_from_template": "standard_relative",
                "created_at": datetime.now().isoformat(),
                "messages": relative_template['initial_conversation'].copy()
            }
            
            user_shopkeeper = {
                "user_id": user_id,
                "persona_type": "shopkeeper",
                "created_from_template": "standard_shopkeeper", 
                "created_at": datetime.now().isoformat(),
                "messages": shopkeeper_template['initial_conversation'].copy()
            }
            
            # Save user-specific personas
            user_folder = os.path.join(self.users_dir, f'user_{user_id}')
            
            with open(os.path.join(user_folder, f'relative_{user_id}.json'), 'w') as f:
                json.dump(user_relative, f, indent=2)
            
            with open(os.path.join(user_folder, f'shopkeeper_{user_id}.json'), 'w') as f:
                json.dump(user_shopkeeper, f, indent=2)
    
    def user_exists(self, user_id):
        """Check if user exists"""
        user_folder = os.path.join(self.users_dir, f'user_{user_id}')
        return os.path.exists(user_folder)
    
    def get_user_conversation(self, user_id, persona_type):
        """Get user's specific persona conversation"""
        user_folder = os.path.join(self.users_dir, f'user_{user_id}')
        conversation_file = os.path.join(user_folder, f'{persona_type}_{user_id}.json')
        
        if os.path.exists(conversation_file):
            with open(conversation_file, 'r') as f:
                return json.load(f)
        return None
    
    def save_user_conversation(self, user_id, persona_type, conversation_data):
        """Save user's conversation"""
        user_folder = os.path.join(self.users_dir, f'user_{user_id}')
        conversation_file = os.path.join(user_folder, f'{persona_type}_{user_id}.json')
        
        with open(conversation_file, 'w') as f:
            json.dump(conversation_data, f, indent=2)
