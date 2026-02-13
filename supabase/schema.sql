-- Items Table
CREATE TABLE items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL,
    base_value DECIMAL NOT NULL,
    image_url TEXT,
    category TEXT,
    rarity TEXT
);

-- Multipliers Table
CREATE TABLE multipliers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    variant_type TEXT NOT NULL,
    multiplier DECIMAL NOT NULL
);

-- Potions Table
CREATE TABLE potions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    add_value DECIMAL NOT NULL
);

-- Row Level Security (RLS)
ALTER TABLE items ENABLE ROW LEVEL SECURITY;
ALTER TABLE multipliers ENABLE ROW LEVEL SECURITY;
ALTER TABLE potions ENABLE ROW LEVEL SECURITY;

-- Policies for items
CREATE POLICY "Public items are viewable by everyone." ON items
    FOR SELECT USING (true);

CREATE POLICY "Items are insertable only by service_role." ON items
    FOR INSERT WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Items are updatable only by service_role." ON items
    FOR UPDATE USING (auth.role() = 'service_role');

CREATE POLICY "Items are deletable only by service_role." ON items
    FOR DELETE USING (auth.role() = 'service_role');

-- Policies for multipliers
CREATE POLICY "Public multipliers are viewable by everyone." ON multipliers
    FOR SELECT USING (true);

CREATE POLICY "Multipliers are insertable only by service_role." ON multipliers
    FOR INSERT WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Multipliers are updatable only by service_role." ON multipliers
    FOR UPDATE USING (auth.role() = 'service_role');

CREATE POLICY "Multipliers are deletable only by service_role." ON multipliers
    FOR DELETE USING (auth.role() = 'service_role');

-- Policies for potions
CREATE POLICY "Public potions are viewable by everyone." ON potions
    FOR SELECT USING (true);

CREATE POLICY "Potions are insertable only by service_role." ON potions
    FOR INSERT WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Potions are updatable only by service_role." ON potions
    FOR UPDATE USING (auth.role() = 'service_role');

CREATE POLICY "Potions are deletable only by service_role." ON potions
    FOR DELETE USING (auth.role() = 'service_role');
