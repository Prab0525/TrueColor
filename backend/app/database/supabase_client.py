"""
Supabase Database Client
Handles all database operations with Supabase
"""

from supabase import create_client, Client
from typing import Optional, List, Dict, Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class SupabaseClient:
    """Supabase database client for TrueShade"""
    
    def __init__(self, use_service_role: bool = False):
        """Initialize Supabase client
        
        Args:
            use_service_role: If True, uses SERVICE_KEY for admin operations (bypasses RLS)
        """
        if not settings.is_supabase_configured:
            logger.warning("⚠️  Supabase not configured. Running in local mode with Python dictionary.")
            logger.warning("   To enable Supabase: Create .env file with SUPABASE_URL and SUPABASE_ANON_KEY")
            self.client: Optional[Client] = None
        else:
            try:
                # Use service role key for admin operations (seeding), anon key for normal operations
                api_key = settings.SUPABASE_SERVICE_KEY if (use_service_role and settings.SUPABASE_SERVICE_KEY) else settings.SUPABASE_ANON_KEY
                
                self.client: Client = create_client(
                    settings.SUPABASE_URL,
                    api_key
                )
                role_type = "SERVICE (admin)" if use_service_role else "ANON (public)"
                logger.info(f"✅ Supabase client initialized successfully ({role_type})")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Supabase: {e}")
                self.client = None
    
    def is_connected(self) -> bool:
        """Check if Supabase is connected"""
        return self.client is not None
    
    # ==================== MAKEUP PRODUCTS ====================
    
    async def get_all_products(self) -> List[Dict[str, Any]]:
        """Get all makeup products from database"""
        if not self.client:
            logger.debug("Using local product database (Supabase not connected)")
            return []
        
        try:
            response = self.client.table("makeup_products").select("*").execute()
            logger.info(f"📦 Retrieved {len(response.data)} products from Supabase")
            return response.data
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            return []
    
    async def get_products_by_brand(self, brand: str) -> List[Dict[str, Any]]:
        """Get products for a specific brand"""
        if not self.client:
            return []
        
        try:
            response = (
                self.client.table("makeup_products")
                .select("*")
                .eq("brand", brand)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching products for {brand}: {e}")
            return []
    
    async def add_product(self, product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Add a new makeup product"""
        if not self.client:
            return None
        
        try:
            response = self.client.table("makeup_products").insert(product_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error adding product: {e}")
            return None
    
    async def clear_all_products(self) -> bool:
        """Clear all products from the database"""
        if not self.client:
            return False
        
        try:
            # Delete all rows by selecting all and deleting
            response = self.client.table("makeup_products").delete().neq("brand", "").execute()
            logger.info(f"✅ Cleared all products from database")
            return True
        except Exception as e:
            logger.error(f"Error clearing products: {e}")
            return False
    
    async def bulk_insert_products(self, products: List[Dict[str, Any]], clear_existing: bool = False) -> bool:
        """Bulk insert makeup products
        
        Args:
            products: List of product dictionaries to insert
            clear_existing: If True, clears existing products before inserting
        """
        if not self.client:
            return False
        
        try:
            # Optionally clear existing products
            if clear_existing:
                logger.info("🗑️  Clearing existing products...")
                await self.clear_all_products()
                logger.info("✅ Existing products cleared")
            
            # Supabase has a limit, so insert in batches
            batch_size = 100
            for i in range(0, len(products), batch_size):
                batch = products[i:i + batch_size]
                self.client.table("makeup_products").insert(batch).execute()
                logger.info(f"📤 Inserted batch {i//batch_size + 1}: {len(batch)} products")
            
            logger.info(f"✅ Successfully inserted {len(products)} total products")
            return True
        except Exception as e:
            logger.error(f"Error bulk inserting products: {e}")
            return False
    
    # ==================== USER PROFILES ====================
    
    async def create_user_profile(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new user profile"""
        if not self.client:
            return None
        
        try:
            response = self.client.table("user_profiles").insert(user_data).execute()
            logger.info(f"👤 Created user profile: {user_data.get('email')}")
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating user profile: {e}")
            return None
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile by ID"""
        if not self.client:
            return None
        
        try:
            response = (
                self.client.table("user_profiles")
                .select("*")
                .eq("id", user_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error fetching user profile: {e}")
            return None
    
    async def update_user_profile(self, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user profile"""
        if not self.client:
            return None
        
        try:
            response = (
                self.client.table("user_profiles")
                .update(update_data)
                .eq("id", user_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error updating user profile: {e}")
            return None
    
    # ==================== ANALYSIS HISTORY ====================
    
    async def save_analysis(self, analysis_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Save a skin tone analysis result"""
        if not self.client:
            logger.debug("Skipping analysis save (Supabase not connected)")
            return None
        
        try:
            response = self.client.table("analysis_history").insert(analysis_data).execute()
            logger.info(f"💾 Saved analysis for user: {analysis_data.get('user_id', 'anonymous')}")
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
            return None
    
    async def get_user_analyses(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get analysis history for a user"""
        if not self.client:
            return []
        
        try:
            response = (
                self.client.table("analysis_history")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching user analyses: {e}")
            return []
    
    async def get_latest_analysis(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get the most recent analysis for a user"""
        if not self.client:
            return None
        
        try:
            response = (
                self.client.table("analysis_history")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error fetching latest analysis: {e}")
            return None
    
    # ==================== USER FAVORITES ====================
    
    async def add_favorite(self, user_id: str, product_id: str) -> Optional[Dict[str, Any]]:
        """Add a product to user's favorites"""
        if not self.client:
            return None
        
        try:
            favorite_data = {
                "user_id": user_id,
                "product_id": product_id
            }
            response = self.client.table("user_favorites").insert(favorite_data).execute()
            logger.info(f"⭐ User {user_id} favorited product {product_id}")
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error adding favorite: {e}")
            return None
    
    async def remove_favorite(self, user_id: str, product_id: str) -> bool:
        """Remove a product from user's favorites"""
        if not self.client:
            return False
        
        try:
            self.client.table("user_favorites").delete().eq("user_id", user_id).eq("product_id", product_id).execute()
            logger.info(f"Removed favorite: user {user_id}, product {product_id}")
            return True
        except Exception as e:
            logger.error(f"Error removing favorite: {e}")
            return False
    
    async def get_user_favorites(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all favorited products for a user"""
        if not self.client:
            return []
        
        try:
            response = (
                self.client.table("user_favorites")
                .select("*, makeup_products(*)")
                .eq("user_id", user_id)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching user favorites: {e}")
            return []


# Global Supabase client instance
supabase_client = SupabaseClient()
