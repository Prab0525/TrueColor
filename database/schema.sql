-- ================================================
-- TrueShade Supabase Database Schema
-- Run this in Supabase SQL Editor
-- ================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ================================================
-- TABLE: makeup_products
-- Stores all makeup product shades with LAB values
-- ================================================
CREATE TABLE IF NOT EXISTS makeup_products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    brand VARCHAR(100) NOT NULL,
    product_line VARCHAR(200) NOT NULL DEFAULT 'Foundation',
    shade_name VARCHAR(200) NOT NULL,
    hex_color VARCHAR(7) NOT NULL,
    lab_l DECIMAL(6, 2) NOT NULL,
    lab_a DECIMAL(6, 2) NOT NULL,
    lab_b DECIMAL(6, 2) NOT NULL,
    undertone VARCHAR(20) CHECK (undertone IN ('warm', 'cool', 'neutral')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Ensure unique combinations
    UNIQUE(brand, product_line, shade_name)
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_makeup_brand ON makeup_products(brand);
CREATE INDEX IF NOT EXISTS idx_makeup_undertone ON makeup_products(undertone);
CREATE INDEX IF NOT EXISTS idx_makeup_lab_l ON makeup_products(lab_l);

-- ================================================
-- TABLE: user_profiles
-- Stores user information and preferences
-- ================================================
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE,
    full_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- User preferences
    preferred_brands TEXT[], -- Array of preferred brands
    skin_type VARCHAR(50),
    allergies TEXT[],
    
    -- Last known skin analysis
    last_skin_lab_l DECIMAL(6, 2),
    last_skin_lab_a DECIMAL(6, 2),
    last_skin_lab_b DECIMAL(6, 2),
    last_undertone VARCHAR(20),
    last_pantone_family VARCHAR(20),
    last_analysis_date TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_user_email ON user_profiles(email);

-- ================================================
-- TABLE: analysis_history
-- Stores all skin tone analysis results
-- ================================================
CREATE TABLE IF NOT EXISTS analysis_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    
    -- Skin tone measurements
    skin_lab_l DECIMAL(6, 2) NOT NULL,
    skin_lab_a DECIMAL(6, 2) NOT NULL,
    skin_lab_b DECIMAL(6, 2) NOT NULL,
    undertone VARCHAR(20) NOT NULL,
    pantone_family VARCHAR(20),
    
    -- Recommendations (stored as arrays)
    recommended_fenty TEXT[],
    recommended_nars TEXT[],
    recommended_toofaced TEXT[],
    
    -- Metadata
    image_url TEXT, -- Optional: if storing images in Supabase Storage
    analysis_metadata JSONB, -- Additional analysis data
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_analysis_user ON analysis_history(user_id);
CREATE INDEX IF NOT EXISTS idx_analysis_date ON analysis_history(created_at DESC);

-- ================================================
-- TABLE: user_favorites
-- Stores user's favorite products
-- ================================================
CREATE TABLE IF NOT EXISTS user_favorites (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    product_id UUID REFERENCES makeup_products(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Ensure a user can only favorite a product once
    UNIQUE(user_id, product_id)
);

CREATE INDEX IF NOT EXISTS idx_favorites_user ON user_favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_favorites_product ON user_favorites(product_id);

-- ================================================
-- FUNCTIONS: Auto-update timestamps
-- ================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to tables with updated_at
DROP TRIGGER IF EXISTS update_makeup_products_updated_at ON makeup_products;
CREATE TRIGGER update_makeup_products_updated_at
    BEFORE UPDATE ON makeup_products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_user_profiles_updated_at ON user_profiles;
CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ================================================
-- ROW LEVEL SECURITY (RLS)
-- ================================================

-- Enable RLS
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE analysis_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_favorites ENABLE ROW LEVEL SECURITY;

-- Policies for user_profiles
DROP POLICY IF EXISTS "Users can view their own profile" ON user_profiles;
CREATE POLICY "Users can view their own profile"
    ON user_profiles FOR SELECT
    USING (auth.uid() = id);

DROP POLICY IF EXISTS "Users can update their own profile" ON user_profiles;
CREATE POLICY "Users can update their own profile"
    ON user_profiles FOR UPDATE
    USING (auth.uid() = id);

DROP POLICY IF EXISTS "Users can insert their own profile" ON user_profiles;
CREATE POLICY "Users can insert their own profile"
    ON user_profiles FOR INSERT
    WITH CHECK (auth.uid() = id);

-- Policies for analysis_history
DROP POLICY IF EXISTS "Users can view their own analysis history" ON analysis_history;
CREATE POLICY "Users can view their own analysis history"
    ON analysis_history FOR SELECT
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert their own analysis" ON analysis_history;
CREATE POLICY "Users can insert their own analysis"
    ON analysis_history FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Policies for user_favorites
DROP POLICY IF EXISTS "Users can view their own favorites" ON user_favorites;
CREATE POLICY "Users can view their own favorites"
    ON user_favorites FOR SELECT
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can manage their own favorites" ON user_favorites;
CREATE POLICY "Users can manage their own favorites"
    ON user_favorites FOR ALL
    USING (auth.uid() = user_id);

-- Public read access to makeup_products (anyone can see products)
DROP POLICY IF EXISTS "Anyone can view makeup products" ON makeup_products;
CREATE POLICY "Anyone can view makeup products"
    ON makeup_products FOR SELECT
    USING (true);

-- ================================================
-- VIEWS: Useful aggregations
-- ================================================

DROP VIEW IF EXISTS popular_products;
CREATE VIEW popular_products AS
SELECT 
    p.id,
    p.brand,
    p.shade_name,
    p.hex_color,
    p.undertone,
    COUNT(f.id) as favorite_count
FROM makeup_products p
LEFT JOIN user_favorites f ON p.id = f.product_id
GROUP BY p.id, p.brand, p.shade_name, p.hex_color, p.undertone
ORDER BY favorite_count DESC;

-- ================================================
-- COMMENTS
-- ================================================
COMMENT ON TABLE makeup_products IS 'Stores all available makeup products with their LAB color values';
COMMENT ON TABLE user_profiles IS 'User account information and preferences';
COMMENT ON TABLE analysis_history IS 'Historical record of all skin tone analyses';
COMMENT ON TABLE user_favorites IS 'User-favorited makeup products';

-- ================================================
-- SUCCESS MESSAGE
-- ================================================
DO $$ 
BEGIN 
    RAISE NOTICE '✅ TrueShade database schema created successfully!';
    RAISE NOTICE '📊 Tables created: makeup_products, user_profiles, analysis_history, user_favorites';
    RAISE NOTICE '🔒 Row Level Security enabled';
    RAISE NOTICE '📝 Next step: Run seed.py to populate makeup products';
END $$;
