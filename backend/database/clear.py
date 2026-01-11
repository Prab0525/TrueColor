"""
Clear all products from Supabase
Run this before seeding
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.supabase_client import SupabaseClient

async def main():
    print("\n🗑️  Clearing all products from Supabase...")
    
    client = SupabaseClient(use_service_role=True)
    
    if not client.is_connected():
        print("❌ Not connected to Supabase")
        return
    
    # Get all products
    products = await client.get_all_products()
    print(f"Found {len(products)} products to delete")
    
    if len(products) == 0:
        print("✅ No products to delete")
        return
    
    # Delete each product individually
    for i, product in enumerate(products, 1):
        try:
            client.client.table("makeup_products").delete().eq("id", product["id"]).execute()
            print(f"  Deleted {i}/{len(products)}: {product['brand']} - {product['shade_name']}")
        except Exception as e:
            print(f"  Error deleting product {i}: {e}")
    
    print(f"\n✅ Successfully cleared all products!")

if __name__ == "__main__":
    asyncio.run(main())
