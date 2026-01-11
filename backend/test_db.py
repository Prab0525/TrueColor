import asyncio
from app.database.supabase_client import SupabaseClient

async def main():
    client = SupabaseClient(use_service_role=True)
    products = await client.get_all_products()
    print(f"\n✅ Found {len(products)} products in Supabase")
    if products:
        print(f"\nFirst product: {products[0]['brand']} - {products[0]['shade_name']}")

if __name__ == "__main__":
    asyncio.run(main())
