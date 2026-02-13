import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export type Variant = 'Regular' | 'Neon' | 'Mega';
export type Potion = 'Fly' | 'Ride';

export interface TradeItem {
    id: string;
    name: string;
    base_value: number;  // Original immutable price
    value: number;       // Calculated price (base * variant + potions) * demand
    image: string;
    rarity?: string;
    demand: number;      // 1-3 (Low/Mid/High)
    variant: Variant;
    potions: Potion[];
}

// --- Value calculation constants ---
const VARIANT_MULTIPLIERS: Record<Variant, number> = {
    Regular: 1,
    Neon: 3,
    Mega: 9,
};

const POTION_BONUSES: Record<Potion, number> = {
    Fly: 0.05,
    Ride: 0.03,
};

const DEMAND_MULTIPLIERS: Record<number, number> = {
    3: 1.15, // High demand bonus
    2: 1.0,  // Normal
    1: 0.85, // Low demand penalty
};

export function calculateValue(baseValue: number, variant: Variant, potions: Potion[], demand: number = 2): number {
    const variantValue = baseValue * VARIANT_MULTIPLIERS[variant];
    const potionBonus = potions.reduce((sum, p) => sum + POTION_BONUSES[p], 0);
    const demandMult = DEMAND_MULTIPLIERS[demand] ?? 1.0;

    return Math.round(((variantValue + potionBonus) * demandMult) * 100) / 100;
}

interface TradeState {
    myItems: TradeItem[];
    theirItems: TradeItem[];
    showDemand: boolean;
    toggleDemand: () => void;
    addItem: (side: 'me' | 'them', item: Omit<TradeItem, 'id' | 'variant' | 'potions' | 'value'>) => void;
    updateItem: (side: 'me' | 'them', id: string, updates: Partial<Pick<TradeItem, 'variant' | 'potions'>>) => void;
    removeItem: (side: 'me' | 'them', id: string) => void;
    clearTrade: () => void;
}

export const useTradeStore = create<TradeState>()(
    persist(
        (set) => ({
            myItems: [],
            theirItems: [],
            showDemand: true,
            toggleDemand: () => set((state) => ({ showDemand: !state.showDemand })),
            addItem: (side, item) => set((state) => {
                // Ensure demand has a fallback if missing from source, default to 2 (Mid)
                const demand = item.demand || 2;
                const variant: Variant = 'Regular';
                const potions: Potion[] = [];
                const newItem: TradeItem = {
                    ...item,
                    id: crypto.randomUUID(),
                    variant,
                    potions,
                    demand,
                    value: calculateValue(item.base_value, variant, potions, demand),
                };
                if (side === 'me') {
                    return { myItems: [...state.myItems, newItem] };
                } else {
                    return { theirItems: [...state.theirItems, newItem] };
                }
            }),
            updateItem: (side, id, updates) => set((state) => {
                const list = side === 'me' ? 'myItems' : 'theirItems';
                return {
                    [list]: state[list].map(item => {
                        if (item.id !== id) return item;
                        const newVariant = updates.variant ?? item.variant;
                        const newPotions = updates.potions ?? item.potions;
                        // Demand doesn't change on update, but is needed for calc
                        return {
                            ...item,
                            variant: newVariant,
                            potions: newPotions,
                            value: calculateValue(item.base_value, newVariant, newPotions, item.demand),
                        };
                    })
                };
            }),
            removeItem: (side, id) => set((state) => {
                if (side === 'me') {
                    return { myItems: state.myItems.filter((i) => i.id !== id) };
                } else {
                    return { theirItems: state.theirItems.filter((i) => i.id !== id) };
                }
            }),
            clearTrade: () => set({ myItems: [], theirItems: [] }),
        }),
        {
            name: 'adopt-me-trade-storage',
            storage: createJSONStorage(() => localStorage),
            version: 3, // Bump version to force recalc or migration
            migrate: (persisted: unknown, version: number) => {
                if (version < 3) {
                    // Previous data might have optional demand or old calculated values
                    // Simplest strategy: reset again to ensure clean state with new math
                    return { myItems: [], theirItems: [], showDemand: true };
                }
                return persisted as TradeState;
            },
        }
    )
);
