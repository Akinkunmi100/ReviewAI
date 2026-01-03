"""
Gadget Category Detection Utility.
Detects product category from name to enable category-specific analysis.
"""

from typing import Optional

# Gadget category keywords
GADGET_CATEGORIES = {
    "phone": [
        "iphone", "galaxy", "pixel", "android", "smartphone", "mobile phone",
        "redmi", "poco", "oneplus", "oppo", "vivo", "realme", "huawei", 
        "samsung phone", "tecno", "infinix", "itel"
    ],
    "laptop": [
        "laptop", "macbook", "thinkpad", "chromebook", "notebook", "ultrabook",
        "dell xps", "hp pavilion", "lenovo", "asus", "acer", "msi laptop",
        "surface laptop", "elitebook"
    ],
    "tablet": [
        "ipad", "galaxy tab", "tablet", "surface pro", "fire tablet"
    ],
    "tv": [
        "tv", "television", "oled tv", "qled", "smart tv", "led tv",
        "samsung tv", "lg tv", "sony tv", "hisense"
    ],
    "headphones": [
        "headphone", "earbuds", "airpods", "wireless earbuds", "headset",
        "sony wh", "bose", "beats", "jbl", "sennheiser", "audio technica"
    ],
    "camera": [
        "camera", "dslr", "mirrorless", "canon eos", "nikon", "sony alpha",
        "fujifilm", "gopro", "action camera"
    ],
    "smartwatch": [
        "smartwatch", "apple watch", "galaxy watch", "fitness tracker",
        "fitbit", "garmin", "amazfit", "band"
    ],
    "speaker": [
        "speaker", "soundbar", "bluetooth speaker", "home theater",
        "boombox", "portable speaker", "jbl speaker", "sonos"
    ],
    "gaming": [
        "playstation", "xbox", "nintendo", "gaming console", "ps5", "ps4",
        "switch", "controller", "gaming headset"
    ]
}

# Critical features per category
CATEGORY_FEATURES = {
    "phone": {
        "battery": ["battery", "mah", "charge", "lasting", "endurance", "power bank"],
        "camera": ["camera", "megapixel", "mp", "lens", "photo", "video", "night mode", "selfie"],
        "performance": ["ram", "processor", "snapdragon", "chip", "speed", "lag", "mediatek", "exynos"],
        "display": ["screen", "display", "amoled", "refresh rate", "hz", "bright", "resolution"],
        "storage": ["storage", "gb", "memory", "rom", "expandable"],
        "charging": ["charger", "charging", "fast charge", "watt", "wireless charging"]
    },
    "laptop": {
        "battery": ["battery", "lasting", "hours", "endurance", "battery life"],
        "display": ["screen", "display", "resolution", "ips", "oled", "bright", "inch"],
        "processor": ["cpu", "processor", "core", "i5", "i7", "i9", "intel", "amd", "ryzen", 
                      "generation", "gen", "ghz", "speed", "m1", "m2", "m3"],
        "storage": ["ssd", "hard drive", "nvme", "storage", "gb", "tb"],
        "ram": ["ram", "memory", "ddr4", "ddr5"],
        "build": ["build", "aluminium", "plastic", "weight", "portable", "thin", "light"],
        "keyboard": ["keyboard", "trackpad", "keys", "typing", "backlighting"],
        "compatibility": ["windows", "macos", "linux", "software", "compatible", "ports", "usb"]
    },
    "tablet": {
        "battery": ["battery", "mah", "lasting"],
        "display": ["screen", "display", "retina", "resolution"],
        "performance": ["chip", "processor", "ram"],
        "storage": ["storage", "gb"],
        "stylus": ["pencil", "stylus", "drawing", "note-taking"]
    },
    "tv": {
        "display": ["screen", "resolution", "4k", "8k", "hdr", "oled", "qled", "brightness"],
        "smart_features": ["smart tv", "apps", "streaming", "voice", "alexa", "google"],
        "audio": ["sound", "speaker", "dolby", "audio"],
        "size": ["inch", "size", "big", "large"]
    },
    "headphones": {
        "sound": ["sound", "audio", "bass", "treble", "noise cancellation", "anc"],
        "battery": ["battery", "hours", "playtime", "charging case"],
        "comfort": ["comfort", "fit", "ear", "cushion", "lightweight"],
        "connectivity": ["bluetooth", "wireless", "multipoint", "range"]
    },
    "camera": {
        "sensor": ["megapixel", "sensor", "full frame", "aps-c", "resolution"],
        "lens": ["lens", "zoom", "aperture", "f/"],
        "video": ["video", "4k", "8k", "fps", "stabilization"],
        "autofocus": ["autofocus", "focus", "af", "tracking"]
    },
    "smartwatch": {
        "battery": ["battery", "days", "charging"],
        "health": ["heart rate", "spo2", "sleep", "fitness", "steps", "calories"],
        "display": ["display", "amoled", "always-on"],
        "features": ["gps", "nfc", "water resistant", "notifications"]
    }
}

# Universal features for ALL products
UNIVERSAL_FEATURES = {
    "durability": ["durable", "lasting", "repair", "break", "lifespan", "warranty", 
                   "years", "sturdy", "robust", "fragile", "crack", "damage"],
    "value": ["price", "value", "worth", "expensive", "cheap", "cost", "affordable"],
    "quality": ["quality", "build", "material", "premium", "solid"]
}


def detect_gadget_category(product_name: str) -> Optional[str]:
    """
    Detect the gadget category from product name.
    
    Args:
        product_name: Name of the product
        
    Returns:
        Category string (phone, laptop, tablet, etc.) or None if not a gadget
    """
    name_lower = product_name.lower()
    
    for category, keywords in GADGET_CATEGORIES.items():
        for keyword in keywords:
            if keyword in name_lower:
                return category
    
    return None


def get_category_features(category: Optional[str]) -> dict:
    """
    Get the critical features to analyze for a category.
    
    Args:
        category: Product category (phone, laptop, etc.) or None
        
    Returns:
        Dictionary of feature aspects and their keywords
    """
    features = UNIVERSAL_FEATURES.copy()
    
    if category and category in CATEGORY_FEATURES:
        features.update(CATEGORY_FEATURES[category])
    
    return features


def get_category_prompt_instructions(product_name: str) -> str:
    """
    Generate LLM prompt instructions for category-specific analysis.
    
    Args:
        product_name: Name of the product
        
    Returns:
        Instruction string for LLM prompt
    """
    category = detect_gadget_category(product_name)
    
    # Universal durability instruction
    base_instruction = """
DURABILITY ASSESSMENT (required for all products):
- Check for mentions of build quality, lifespan, and repair frequency
- Note warranty information if available
- Flag durability concerns if reviews mention breakage or repairs
"""
    
    if category == "phone":
        return base_instruction + """
CRITICAL PHONE FEATURES to analyze:
- Battery: Capacity (mAh), charging speed, real-world battery life
- Camera: Megapixels, lens count, photo/video quality, night mode
- Performance: RAM, processor (Snapdragon/MediaTek/Exynos), speed
- Display: Size, type (AMOLED/LCD), refresh rate (Hz), brightness
- Storage: Capacity options, expandable storage
"""
    
    elif category == "laptop":
        return base_instruction + """
CRITICAL LAPTOP FEATURES to analyze:
- Processor: Core count, generation (e.g., 12th Gen i7), speed (GHz)
- RAM: Capacity, type (DDR4/DDR5), upgradability
- Storage: SSD type (NVMe/SATA), capacity, speed
- Display: Size, resolution, panel type, refresh rate
- Battery: Real-world hours of use
- Compatibility: OS support, ports (USB-C, HDMI, etc.)
- Build: Weight, material, keyboard quality
"""
    
    elif category == "tablet":
        return base_instruction + """
CRITICAL TABLET FEATURES to analyze:
- Display: Size, resolution, refresh rate
- Performance: Chip, RAM
- Battery: Capacity, usage time
- Stylus support and functionality
- Storage options
"""
    
    elif category == "tv":
        return base_instruction + """
CRITICAL TV FEATURES to analyze:
- Display: Resolution (4K/8K), panel type (OLED/QLED), HDR support
- Size: Screen size in inches
- Smart features: OS, apps, streaming support
- Audio: Built-in speaker quality
"""
    
    elif category == "headphones":
        return base_instruction + """
CRITICAL HEADPHONE FEATURES to analyze:
- Sound quality: Bass, treble, clarity
- Noise cancellation: ANC capability
- Battery: Playtime hours, case charging
- Comfort: Fit, weight, ear cushions
- Connectivity: Bluetooth version, multipoint
"""
    
    elif category == "camera":
        return base_instruction + """
CRITICAL CAMERA FEATURES to analyze:
- Sensor: Megapixels, sensor size
- Video: Resolution, frame rates
- Lens: Aperture, zoom capability
- Autofocus: Speed, accuracy
"""
    
    elif category == "smartwatch":
        return base_instruction + """
CRITICAL SMARTWATCH FEATURES to analyze:
- Battery: Days of use per charge
- Health tracking: Heart rate, SpO2, sleep, fitness
- Display: Type, always-on capability
- Features: GPS, NFC, water resistance
"""
    
    else:
        return base_instruction
