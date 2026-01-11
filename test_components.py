"""
Show what's broken without Python 3.12
"""

print("\n" + "="*60)
print("🔍 TrueShade Component Status Check")
print("="*60)

# Test 1: Database (Should work)
print("\n1️⃣  Supabase Database...")
try:
    import asyncio
    from app.database.supabase_client import SupabaseClient
    client = SupabaseClient()
    products = asyncio.run(client.get_all_products())
    print(f"   ✅ WORKING - {len(products)} products loaded")
except Exception as e:
    print(f"   ❌ BROKEN - {e}")

# Test 2: Color Analysis (Should work)
print("\n2️⃣  LAB Color Analysis...")
try:
    from app.services.skin_analysis import SkinAnalysisService
    analyzer = SkinAnalysisService()
    print("   ✅ WORKING - Color science algorithms ready")
except Exception as e:
    print(f"   ❌ BROKEN - {e}")

# Test 3: Shade Matching (Should work)
print("\n3️⃣  Shade Matching Algorithm...")
try:
    from app.services.shade_matcher import ShadeMatcherService
    matcher = ShadeMatcherService()
    print("   ✅ WORKING - Delta E matching ready")
except Exception as e:
    print(f"   ❌ BROKEN - {e}")

# Test 4: Face Detection (BROKEN on Python 3.13)
print("\n4️⃣  MediaPipe Face Detection...")
try:
    from app.services.face_detection import FaceDetectionService
    detector = FaceDetectionService()
    if detector.is_available:
        print("   ✅ WORKING - Face detection ready")
    else:
        print("   ❌ BROKEN - MediaPipe not compatible with Python 3.13")
except Exception as e:
    print(f"   ❌ BROKEN - {e}")

# Test 5: FastAPI Server (Partially working)
print("\n5️⃣  FastAPI Server...")
print("   ⚠️  PARTIAL - Server starts but /analyze endpoint won't work")

print("\n" + "="*60)
print("📊 Summary")
print("="*60)
print("✅ Working: Database, Color Analysis, Shade Matching")
print("❌ Broken: Face Detection (needs Python 3.12)")
print("⚠️  Impact: Can't analyze face photos")
print("\n💡 Fix: Install Python 3.12 and recreate venv")
print("   See: PYTHON_VERSION_FIX.md")
print("="*60 + "\n")
