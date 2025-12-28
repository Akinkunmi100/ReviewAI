"""
Quick Test Script - Check if Image Fetching Works

Run this to quickly test if your image fetching is working at all.
This will show you exactly what's happening.
"""

import os
import sys

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("="*80)
print("QUICK IMAGE FETCH TEST")
print("="*80)

# Step 1: Check environment
print("\n1️⃣ Checking environment...")
from dotenv import load_dotenv
load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    print("   ❌ GROQ_API_KEY not found in .env")
    print("   → Add your API key to .env file")
    sys.exit(1)
else:
    print("   ✅ GROQ_API_KEY found")

# Step 2: Import modules
print("\n2️⃣ Importing modules...")
try:
    from app_update import (
        EnhancedProductReviewService,
        ProductImageFetcher,
        CacheManager,
        AppConfig
    )
    print("   ✅ Modules imported successfully")
except Exception as e:
    print(f"   ❌ Import error: {e}")
    sys.exit(1)

# Step 3: Test image fetcher directly
print("\n3️⃣ Testing image fetcher directly...")
try:
    config = AppConfig()
    cache = CacheManager()
    fetcher = ProductImageFetcher(cache, config)
    
    test_product = "iPhone 16 Pro Max"
    print(f"   Testing: {test_product}")
    
    images = fetcher.fetch_product_images(test_product, max_images=3)
    
    if images:
        print(f"   ✅ Found {len(images)} images:")
        for idx, img in enumerate(images, 1):
            print(f"      {idx}. {img.source}")
            print(f"         URL: {img.url[:80]}...")
    else:
        print(f"   ⚠️ No images found")
        print("   → This means either:")
        print("      a) Web sources don't have this product")
        print("      b) Images failed strict validation")
        print("      c) Network/scraping issue")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Step 4: Test full review generation
print("\n4️⃣ Testing full review generation...")
try:
    service = EnhancedProductReviewService(groq_key)
    print("   Service initialized")
    
    print(f"   Generating review for: {test_product}")
    print("   (This will take 15-30 seconds...)")
    
    review = service.generate_review(test_product, use_web_search=True)
    
    print(f"\n   ✅ Review generated!")
    print(f"      Product: {review.product_name}")
    print(f"      Rating: {review.predicted_rating}")
    
    # Check images in review
    has_images = hasattr(review, 'product_images')
    has_primary = hasattr(review, 'primary_image_url') and review.primary_image_url
    
    if has_images:
        num_images = len(review.product_images)
        print(f"      Images: {num_images} found")
        
        if num_images > 0:
            print(f"\n      📸 Image URLs:")
            for idx, img in enumerate(review.product_images[:3], 1):
                print(f"         {idx}. {img.url[:80]}...")
        
        if has_primary:
            print(f"\n      ✨ Primary image set:")
            print(f"         {review.primary_image_url[:80]}...")
        else:
            print(f"\n      ⚠️ Primary image NOT set (but {num_images} images exist)")
    else:
        print(f"      ❌ No images in review object")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Step 5: Summary and next steps
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

print("""
What to check:
1. If "No images found" in Step 3:
   → Images are being strictly filtered (see SOLUTIONS_FOR_IMAGE_ISSUE.md)
   → Consider Options B, C, or D from that document

2. If "Images found" but "Primary image NOT set":
   → Check EnhancedReviewGenerator.generate_enhanced_review()
   → Ensure: review.primary_image_url = product_images[0].url if product_images else None

3. If everything works here but not in frontend:
   → Check React frontend is calling /api/review correctly
   → Check DecisionCard.tsx is displaying primary_image_url
   → Open browser DevTools → Network → Check image URLs

Next steps:
- Read: SOLUTIONS_FOR_IMAGE_ISSUE.md for detailed solutions
- Try: Different test products to see consistency
- Run: Backend (uvicorn api:app) and frontend (npm run dev) to test end-to-end
""")

print("="*80)
print("Test complete!")
print("="*80)
