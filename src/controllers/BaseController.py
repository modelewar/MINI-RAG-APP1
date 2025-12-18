from helpers.config import get_settings , Settings
import os
import random
import string
class BaseController:
    def __init__(self):
        
        self.app_settings:Settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_dir = os.path.join(
            self.base_dir, 'assets/files'
        )
    
    def generate_random_string(self, length: int = 12):
        """
        Generates a random string of lowercase letters and digits.
        Used for creating unique filenames for RAG data uploads.
        """
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))     