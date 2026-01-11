"""
Database Seed Script
Migrates local makeup database to Supabase
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.data.makeup_database import MAKEUP_DATABASE
from app.database.supabase_client import SupabaseClient

# Create admin client for seeding (uses SERVICE_KEY)
supabase_client = SupabaseClient(use_service_role=True)


async def seed_makeup_products():
    """Seed makeup products into Supabase"""
    
    if not supabase_client.is_connected():
        print("\n" + "="*60)
        print("❌ Supabase not connected")
        print("="*60)
        print("\n📝 To configure Supabase:")
        print("  1. Create account at https://supabase.com")
        print("  2. Create a new project")
        print("  3. Copy .env.example to .env")
        print("  4. Add your SUPABASE_URL and SUPABASE_ANON_KEY to .env")
        print("  5. Run database/schema.sql in Supabase SQL Editor")
        print("  6. Run this script again\n")
        return False
    
    print("\n" + "="*60)
    print("🌱 TrueShade Database Seeder")
    print("="*60)
    
    # Check if products already exist
    existing_products = await supabase_client.get_all_products()
    if existing_products:
        print(f"\n✅ Database already seeded with {len(existing_products)} products!")
        print("\n📊 Products by brand:")
        for brand in ["Fenty", "Nars", "Too Faced"]:
            brand_products = await supabase_client.get_products_by_brand(brand)
            print(f"   • {brand}: {len(brand_products)} shades")
        print("\n💡 To re-seed, manually delete products in Supabase Table Editor first.")
        return True
    
    total_products = sum(len(shades) for shades in MAKEUP_DATABASE.values())
    print(f"\n📦 Preparing to migrate {total_products} makeup products...")
    
    all_products = []
    
    # Convert local database to Supabase format
    for brand, shades in MAKEUP_DATABASE.items():
        brand_name = "Too Faced" if brand == "tooFaced" else brand.title()
        
        for shade in shades:
            lab = shade["lab"]
            
            product = {
                "brand": brand_name,
                "product_line": f"{brand_name} Pro Filt'r Foundation" if brand == "fenty" 
                               else f"{brand_name} Foundation",
                "shade_name": shade["name"],
                "hex_color": shade["hex"],
                "lab_l": float(lab[0]),
                "lab_a": float(lab[1]),
                "lab_b": float(lab[2]),
                "undertone": shade["undertone"]
            }
            all_products.append(product)
    
    # Bulk insert
    print(f"\n📤 Uploading {len(all_products)} products to Supabase...")
    print("   (This may take a moment...)")
    
    success = await supabase_client.bulk_insert_products(all_products, clear_existing=True)
    
    if success:
        print(f"\n✅ Successfully seeded {len(all_products)} makeup products!")
        print("\n📊 Breakdown by brand:")
        for brand, shades in MAKEUP_DATABASE.items():
            brand_name = "Too Faced" if brand == "tooFaced" else brand.title()
            print(f"   • {brand_name}: {len(shades)} shades")
        return True
    else:
        print("\n❌ Failed to seed products")
        print("   Check your Supabase connection and schema")
        return False


async def verify_seed():
    """Verify the seed was successful"""
    
    if not supabase_client.is_connected():
        return False
    
    print("\n" + "-"*60)
    print("🔍 Verifying seed...")
    print("-"*60)
    
    products = await supabase_client.get_all_products()
    print(f"\n✅ Found {len(products)} products in database")
    
    if len(products) > 0:
        print("\n📊 Products by brand:")
        for brand in ["Fenty", "Nars", "Too Faced"]:
            brand_products = await supabase_client.get_products_by_brand(brand)
            print(f"   • {brand}: {len(brand_products)} shades")
        
        # Show sample products
        print("\n🎨 Sample products:")
        for i, product in enumerate(products[:3]):
            print(f"   {i+1}. {product['brand']} - {product['shade_name']} ({product['hex_color']})")
    
    return True


async def main():
    """Main seed function"""
    
    # Seed products
    success = await seed_makeup_products()
    
    if not success:
        sys.exit(1)
    
    # Verify
    await verify_seed()
    
    print("\n" + "="*60)
    print("✅ Database seeding complete!")
    print("="*60)
    print("\n🚀 Your TrueShade backend is now connected to Supabase!")
    print("   You can now run: python run.py\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Seeding interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
