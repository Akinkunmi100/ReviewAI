"""
Debug script to test image fetching for specific products
Run this to see exactly what images are being fetched and why
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dot

env
load_dotenv()

from app_update import (
    ProductImageFetcher,
    CacheManager,
    AppConfig,
    EnhancedProductReviewService
)

def test_image_fetching():
    """Test image fetching for various products"""
    
    # Initialize service
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("❌ GROQ_API_KEY not found in .env file")
        return
    
    config = AppConfig()
    cache_manager = CacheManager()
    image_fetcher = ProductImageFetcher(cache_manager, config)
    
    # Test products
    test_products = [
        "iPhone 16 Pro Max",
        "Samsung Galaxy S24 Ultra",
        "MacBook Pro M3 14-inch",
        "Sony WH-1000XM5",
        "Nintendo Switch OLED",
        "Tecno Camon 30 Pro"
    ]
    
    print("="*80)
    print("IMAGE FETCHING DEBUG TEST")
    print("="*80)
    
    for product_name in test_products:
        print(f"\n📱 Testing: {product_name}")
        print("-"*80)
        
        try:
            images = image_fetcher.fetch_product_images(product_name, max_images=5)
            
            if not images:
                print(f"❌ No images found for '{product_name}'")
                print("   This means:")
                print("   1. Web sources don't have images, OR")
                print("   2. Found images failed strict validation (better than wrong images!)")
            else:
                print(f"✅ Found {len(images)} validated images:")
                for idx, img in enumerate(images, 1):
                    print(f"\n   {idx}. Source: {img.source}")
                    print(f"      URL: {img.url[:100]}...")
                    if img.alt_text:
                        print(f"      Alt: {img.alt_text[:80]}...")
                
                # Show primary image
                print(f"\n   ✨ PRIMARY IMAGE:")
                print(f"      {images[0].url}")
                
        except Exception as e:
            print(f"❌ Error fetching images: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("Test complete!")
    print("="*80)

def test_single_product_review():
    """Test full review generation including images"""
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("❌ GROQ_API_KEY not found in .env file")
        return
    
    service = EnhancedProductReviewService(groq_api_key)
    
    product = input("\nEnter product name to test (or press Enter for 'iPhone 16 Pro'): ").strip()
    if not product:
        product = "iPhone 16 Pro"
    
    print(f"\n🔍 Generating full review for: {product}")
    print("="*80)
    
    try:
        review = service.generate_review(product, use_web_search=True)
        
        print(f"\n✅ Review generated successfully!")
        print(f"   Product: {review.product_name}")
        print(f"   Rating: {review.predicted_rating}")
        print(f"   Images found: {len(review.product_images) if hasattr(review, 'product_images') else 0}")
        
        if hasattr(review, 'primary_image_url') and review.primary_image_url:
            print(f"\n   ✨ PRIMARY IMAGE:")
            print(f"      {review.primary_image_url}")
        else:
            print(f"\n   ❌ No primary image set")
        
        # Show all images
        if hasattr(review, 'product_images') and review.product_images:
            print(f"\n   📸 ALL IMAGES:")
            for idx, img in enumerate(review.product_images, 1):
                print(f"      {idx}. {img.source}: {img.url[:80]}...")
        
    except Exception as e:
        print(f"❌ Error generating review: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\n" + "="*80)
    print("PRODUCT IMAGE FETCHING DEBUG TOOL")
    print("="*80)
    print("\nOptions:")
    print("1. Test image fetching only (fast)")
    print("2. Test full review generation (includes images, slower)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_image_fetching()
    elif choice == "2":
        test_single_product_review()
    else:
        print("Invalid choice")
