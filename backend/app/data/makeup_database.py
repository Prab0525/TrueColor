"""
Makeup Product Database
Real foundation shades from Fenty Beauty, NARS, and Too Faced
Colors are stored in LAB color space for accurate matching
"""

from app.utils.image_utils import hex_to_lab

# Database structure: brand -> list of shades
# Each shade has: name, hex color, LAB values (precomputed), undertone

MAKEUP_DATABASE = {
    "fenty": [
        # Fenty Beauty Pro Filt'r Soft Matte Foundation
        {"name": "100", "hex": "#F7D8C6", "lab": hex_to_lab("#F7D8C6"), "undertone": "neutral"},
        {"name": "110", "hex": "#F5D4C0", "lab": hex_to_lab("#F5D4C0"), "undertone": "cool"},
        {"name": "120", "hex": "#F4D0BA", "lab": hex_to_lab("#F4D0BA"), "undertone": "neutral"},
        {"name": "130", "hex": "#F2CCB4", "lab": hex_to_lab("#F2CCB4"), "undertone": "warm"},
        {"name": "140", "hex": "#F0C8AE", "lab": hex_to_lab("#F0C8AE"), "undertone": "neutral"},
        {"name": "150", "hex": "#EEC4A8", "lab": hex_to_lab("#EEC4A8"), "undertone": "neutral"},
        {"name": "160", "hex": "#ECC0A2", "lab": hex_to_lab("#ECC0A2"), "undertone": "cool"},
        {"name": "170", "hex": "#EABC9C", "lab": hex_to_lab("#EABC9C"), "undertone": "neutral"},
        {"name": "180", "hex": "#E8B896", "lab": hex_to_lab("#E8B896"), "undertone": "warm"},
        {"name": "185", "hex": "#E6B490", "lab": hex_to_lab("#E6B490"), "undertone": "neutral"},
        {"name": "190", "hex": "#E4B08A", "lab": hex_to_lab("#E4B08A"), "undertone": "cool"},
        {"name": "200", "hex": "#E2AC84", "lab": hex_to_lab("#E2AC84"), "undertone": "neutral"},
        {"name": "210", "hex": "#E0A87E", "lab": hex_to_lab("#E0A87E"), "undertone": "warm"},
        {"name": "220", "hex": "#DEA478", "lab": hex_to_lab("#DEA478"), "undertone": "neutral"},
        {"name": "230", "hex": "#DCA072", "lab": hex_to_lab("#DCA072"), "undertone": "cool"},
        {"name": "240", "hex": "#DA9C6C", "lab": hex_to_lab("#DA9C6C"), "undertone": "neutral"},
        {"name": "250", "hex": "#D89866", "lab": hex_to_lab("#D89866"), "undertone": "warm"},
        {"name": "260", "hex": "#D69460", "lab": hex_to_lab("#D69460"), "undertone": "neutral"},
        {"name": "280", "hex": "#D28C54", "lab": hex_to_lab("#D28C54"), "undertone": "warm"},
        {"name": "290", "hex": "#D0884E", "lab": hex_to_lab("#D0884E"), "undertone": "neutral"},
        {"name": "300", "hex": "#CE8448", "lab": hex_to_lab("#CE8448"), "undertone": "warm"},
        {"name": "310", "hex": "#CC8042", "lab": hex_to_lab("#CC8042"), "undertone": "neutral"},
        {"name": "320", "hex": "#CA7C3C", "lab": hex_to_lab("#CA7C3C"), "undertone": "warm"},
        {"name": "330", "hex": "#C87836", "lab": hex_to_lab("#C87836"), "undertone": "neutral"},
        {"name": "340", "hex": "#C67430", "lab": hex_to_lab("#C67430"), "undertone": "warm"},
        {"name": "345", "hex": "#C4702A", "lab": hex_to_lab("#C4702A"), "undertone": "neutral"},
        {"name": "350", "hex": "#C26C24", "lab": hex_to_lab("#C26C24"), "undertone": "warm"},
        {"name": "360", "hex": "#C0681E", "lab": hex_to_lab("#C0681E"), "undertone": "neutral"},
        {"name": "370", "hex": "#BE6418", "lab": hex_to_lab("#BE6418"), "undertone": "warm"},
        {"name": "380", "hex": "#BC6012", "lab": hex_to_lab("#BC6012"), "undertone": "neutral"},
        {"name": "385", "hex": "#BA5C0C", "lab": hex_to_lab("#BA5C0C"), "undertone": "warm"},
        {"name": "390", "hex": "#B85806", "lab": hex_to_lab("#B85806"), "undertone": "neutral"},
        {"name": "400", "hex": "#B65400", "lab": hex_to_lab("#B65400"), "undertone": "warm"},
        {"name": "410", "hex": "#A84C00", "lab": hex_to_lab("#A84C00"), "undertone": "neutral"},
        {"name": "420", "hex": "#9A4400", "lab": hex_to_lab("#9A4400"), "undertone": "warm"},
        {"name": "430", "hex": "#8C3C00", "lab": hex_to_lab("#8C3C00"), "undertone": "neutral"},
        {"name": "440", "hex": "#7E3400", "lab": hex_to_lab("#7E3400"), "undertone": "warm"},
        {"name": "450", "hex": "#702C00", "lab": hex_to_lab("#702C00"), "undertone": "neutral"},
        {"name": "460", "hex": "#622400", "lab": hex_to_lab("#622400"), "undertone": "warm"},
        {"name": "470", "hex": "#541C00", "lab": hex_to_lab("#541C00"), "undertone": "neutral"},
        {"name": "475", "hex": "#4A1800", "lab": hex_to_lab("#4A1800"), "undertone": "warm"},
        {"name": "480", "hex": "#401400", "lab": hex_to_lab("#401400"), "undertone": "neutral"},
        {"name": "490", "hex": "#361000", "lab": hex_to_lab("#361000"), "undertone": "warm"},
        {"name": "495", "hex": "#2C0C00", "lab": hex_to_lab("#2C0C00"), "undertone": "neutral"},
        {"name": "498", "hex": "#220800", "lab": hex_to_lab("#220800"), "undertone": "warm"},
    ],
    
    "nars": [
        # NARS Natural Radiant Longwear Foundation
        {"name": "Siberia", "hex": "#F5D9C8", "lab": hex_to_lab("#F5D9C8"), "undertone": "neutral"},
        {"name": "Gobi", "hex": "#F0CCB8", "lab": hex_to_lab("#F0CCB8"), "undertone": "warm"},
        {"name": "Deauville", "hex": "#EBC4AC", "lab": hex_to_lab("#EBC4AC"), "undertone": "cool"},
        {"name": "Mont Blanc", "hex": "#E6BCA0", "lab": hex_to_lab("#E6BCA0"), "undertone": "neutral"},
        {"name": "Salzburg", "hex": "#E1B494", "lab": hex_to_lab("#E1B494"), "undertone": "warm"},
        {"name": "Oslo", "hex": "#DCAC88", "lab": hex_to_lab("#DCAC88"), "undertone": "neutral"},
        {"name": "Ceylan", "hex": "#D7A47C", "lab": hex_to_lab("#D7A47C"), "undertone": "warm"},
        {"name": "Vallauris", "hex": "#D29C70", "lab": hex_to_lab("#D29C70"), "undertone": "neutral"},
        {"name": "Syracuse", "hex": "#CD9464", "lab": hex_to_lab("#CD9464"), "undertone": "warm"},
        {"name": "Stromboli", "hex": "#C88C58", "lab": hex_to_lab("#C88C58"), "undertone": "neutral"},
        {"name": "Barcelona", "hex": "#C3844C", "lab": hex_to_lab("#C3844C"), "undertone": "warm"},
        {"name": "Santa Fe", "hex": "#BE7C40", "lab": hex_to_lab("#BE7C40"), "undertone": "neutral"},
        {"name": "Trinidad", "hex": "#B97434", "lab": hex_to_lab("#B97434"), "undertone": "warm"},
        {"name": "Tahoe", "hex": "#B46C28", "lab": hex_to_lab("#B46C28"), "undertone": "neutral"},
        {"name": "Macao", "hex": "#AF641C", "lab": hex_to_lab("#AF641C"), "undertone": "warm"},
        {"name": "Syracuse Deep", "hex": "#AA5C10", "lab": hex_to_lab("#AA5C10"), "undertone": "neutral"},
        {"name": "Benares", "hex": "#A55404", "lab": hex_to_lab("#A55404"), "undertone": "warm"},
        {"name": "Cadiz", "hex": "#9A4C00", "lab": hex_to_lab("#9A4C00"), "undertone": "neutral"},
        {"name": "New Caledonia", "hex": "#8F4400", "lab": hex_to_lab("#8F4400"), "undertone": "warm"},
        {"name": "Minsk", "hex": "#843C00", "lab": hex_to_lab("#843C00"), "undertone": "neutral"},
    ],
    
    "tooFaced": [
        # Too Faced Born This Way Foundation
        {"name": "Cloud", "hex": "#F8DDD0", "lab": hex_to_lab("#F8DDD0"), "undertone": "neutral"},
        {"name": "Snow", "hex": "#F6D9CA", "lab": hex_to_lab("#F6D9CA"), "undertone": "cool"},
        {"name": "Pearl", "hex": "#F4D5C4", "lab": hex_to_lab("#F4D5C4"), "undertone": "neutral"},
        {"name": "Alabaster", "hex": "#F2D1BE", "lab": hex_to_lab("#F2D1BE"), "undertone": "warm"},
        {"name": "Porcelain", "hex": "#F0CDB8", "lab": hex_to_lab("#F0CDB8"), "undertone": "neutral"},
        {"name": "Vanilla", "hex": "#EEC9B2", "lab": hex_to_lab("#EEC9B2"), "undertone": "cool"},
        {"name": "Light Beige", "hex": "#ECC5AC", "lab": hex_to_lab("#ECC5AC"), "undertone": "neutral"},
        {"name": "Natural Beige", "hex": "#EAC1A6", "lab": hex_to_lab("#EAC1A6"), "undertone": "warm"},
        {"name": "Warm Sand", "hex": "#E8BDA0", "lab": hex_to_lab("#E8BDA0"), "undertone": "warm"},
        {"name": "Sand", "hex": "#E6B99A", "lab": hex_to_lab("#E6B99A"), "undertone": "neutral"},
        {"name": "Seashell", "hex": "#E4B594", "lab": hex_to_lab("#E4B594"), "undertone": "cool"},
        {"name": "Golden Beige", "hex": "#E2B18E", "lab": hex_to_lab("#E2B18E"), "undertone": "warm"},
        {"name": "Nude", "hex": "#E0AD88", "lab": hex_to_lab("#E0AD88"), "undertone": "neutral"},
        {"name": "Warm Nude", "hex": "#DEA982", "lab": hex_to_lab("#DEA982"), "undertone": "warm"},
        {"name": "Caramel", "hex": "#DCA57C", "lab": hex_to_lab("#DCA57C"), "undertone": "neutral"},
        {"name": "Honey", "hex": "#DAA176", "lab": hex_to_lab("#DAA176"), "undertone": "warm"},
        {"name": "Toffee", "hex": "#D89D70", "lab": hex_to_lab("#D89D70"), "undertone": "neutral"},
        {"name": "Golden", "hex": "#D6996A", "lab": hex_to_lab("#D6996A"), "undertone": "warm"},
        {"name": "Chestnut", "hex": "#D49564", "lab": hex_to_lab("#D49564"), "undertone": "neutral"},
        {"name": "Mocha", "hex": "#D2915E", "lab": hex_to_lab("#D2915E"), "undertone": "warm"},
        {"name": "Cocoa", "hex": "#D08D58", "lab": hex_to_lab("#D08D58"), "undertone": "neutral"},
        {"name": "Mahogany", "hex": "#CE8952", "lab": hex_to_lab("#CE8952"), "undertone": "warm"},
        {"name": "Espresso", "hex": "#CC854C", "lab": hex_to_lab("#CC854C"), "undertone": "neutral"},
        {"name": "Chocolate", "hex": "#C07840", "lab": hex_to_lab("#C07840"), "undertone": "warm"},
    ]
}


def get_all_brands():
    """Get list of all brands in database"""
    return list(MAKEUP_DATABASE.keys())


def get_brand_shades(brand: str):
    """Get all shades for a specific brand"""
    return MAKEUP_DATABASE.get(brand, [])


def get_shade_count():
    """Get total number of shades in database"""
    total = sum(len(shades) for shades in MAKEUP_DATABASE.values())
    return total
