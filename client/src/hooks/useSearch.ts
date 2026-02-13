import { useMemo } from 'react';
import Fuse from 'fuse.js';
import itemsData from '../data/items.json';

export interface SourceItem {
    name: string;
    base_value: number;
    image_url: string;
    category?: string;
    demand?: number;
}

const allItems = itemsData as SourceItem[];

const fuse = new Fuse(allItems, {
    keys: [
        { name: 'name', weight: 2 },
        { name: 'category', weight: 1 },
    ],
    threshold: 0.3,
    includeScore: true,
    minMatchCharLength: 2,
});

export function useSearch(query: string, limit = 12) {
    return useMemo(() => {
        if (!query || query.length < 2) return [];
        return fuse.search(query, { limit }).map((r) => r.item);
    }, [query, limit]);
}
