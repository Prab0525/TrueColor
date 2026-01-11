"""
Application Configuration
Loads environment variables and provides config settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings from environment variables"""
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Supabase settings
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")
    
    # Validation
    @property
    def is_supabase_configured(self) -> bool:
        """Check if Supabase is properly configured"""
        return bool(self.SUPABASE_URL and self.SUPABASE_ANON_KEY)
    
    def get_status(self) -> dict:
        """Get configuration status"""
        return {
            "server_configured": bool(self.HOST and self.PORT),
            "supabase_configured": self.is_supabase_configured,
            "debug_mode": self.DEBUG
        }


settings = Settings()
