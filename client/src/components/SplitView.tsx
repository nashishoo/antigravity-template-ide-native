import { useState } from 'react';
import { useTradeStore, type TradeItem } from '../store/tradeStore';
import { TradeSlot } from './TradeSlot';
import { Plus, Trash2, Settings } from 'lucide-react';
import { WinLoseBar } from './WinLoseBar';
import { SettingsModal } from './SettingsModal';
import { SearchModal } from './SearchModal';
import type { SourceItem } from '../hooks/useSearch';

export function SplitView() {
    const { myItems, theirItems, addItem, removeItem, clearTrade } = useTradeStore();
    const [searchSide, setSearchSide] = useState<'me' | 'them' | null>(null);
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);

    const handleAddItem = (item: SourceItem) => {
        if (searchSide) {
            const tradeItem: Omit<TradeItem, 'id' | 'variant' | 'potions' | 'value'> = {
                name: item.name,
                base_value: item.base_value,
                image: item.image_url,
                rarity: 'Common',
                demand: item.demand ?? 2 // Default to Normal if missing
            };
            addItem(searchSide, tradeItem);
        }
    };

    return (
        <div className="flex flex-col h-screen w-full bg-game-bg text-gray-800 overflow-hidden font-sans">

            {/* HEADER */}
            <header className="p-4 bg-white/80 backdrop-blur-md border-b border-white/20 flex justify-between items-center shadow-sm z-20">
                <h1 className="text-2xl font-black text-gray-800 tracking-tight">
                    <span className="text-game-badge-fly">Adopt</span> <span className="text-game-badge-ride">Me</span> Trade
                </h1>

                <div className="flex gap-2">
                    <button
                        onClick={() => setIsSettingsOpen(true)}
                        className="p-2 bg-white rounded-full text-gray-500 hover:bg-gray-100 shadow-sm transition-colors"
                    >
                        <Settings size={20} />
                    </button>
                    <button
                        onClick={clearTrade}
                        className="p-2 bg-white rounded-full text-game-lose hover:bg-red-50 shadow-sm transition-colors"
                    >
                        <Trash2 size={20} />
                    </button>
                </div>
            </header>

            {/* WIN/LOSE BAR */}
            <div className="bg-white/50 pb-4">
                <WinLoseBar />
            </div>

            {/* MAIN CONTENT - SPLIT VIEW */}
            <div className="flex-1 flex flex-col md:flex-row overflow-hidden relative">

                {/* LEFT PANEL - MY OFFER */}
                <div className="flex-1 flex flex-col border-b md:border-b-0 md:border-r border-gray-200 relative bg-white/30">
                    <div className="p-3 bg-blue-50/80 border-b border-blue-100 flex justify-between items-center">
                        <h2 className="text-lg font-bold text-blue-600">You</h2>
                        <span className="text-sm font-semibold bg-blue-100 text-blue-700 px-2 py-0.5 rounded-md">
                            {myItems.reduce((acc, i) => acc + i.value, 0).toFixed(2)}
                        </span>
                    </div>

                    <div className="flex-1 p-4 grid grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3 content-start overflow-y-auto custom-scrollbar">
                        {myItems.map((item) => (
                            <TradeSlot key={item.id} item={item} side="me" onRemove={() => removeItem('me', item.id)} />
                        ))}
                        <button
                            onClick={() => setSearchSide('me')}
                            className="w-24 h-28 md:w-32 md:h-36 border-2 border-dashed border-blue-300 rounded-2xl flex flex-col items-center justify-center text-blue-300 hover:text-blue-500 hover:border-blue-500 hover:bg-blue-50 transition-all group"
                        >
                            <div className="bg-blue-100 p-2 rounded-full mb-1 group-hover:scale-110 transition-transform">
                                <Plus size={24} className="text-blue-500" />
                            </div>
                            <span className="text-xs font-bold">Add Pet</span>
                        </button>
                    </div>
                </div>

                {/* RIGHT PANEL - THEIR OFFER */}
                <div className="flex-1 flex flex-col relative bg-white/30">
                    <div className="p-3 bg-pink-50/80 border-b border-pink-100 flex justify-between items-center">
                        <h2 className="text-lg font-bold text-pink-600">Them</h2>
                        <span className="text-sm font-semibold bg-pink-100 text-pink-700 px-2 py-0.5 rounded-md">
                            {theirItems.reduce((acc, i) => acc + i.value, 0).toFixed(2)}
                        </span>
                    </div>

                    <div className="flex-1 p-4 grid grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3 content-start overflow-y-auto custom-scrollbar">
                        {theirItems.map((item) => (
                            <TradeSlot key={item.id} item={item} side="them" onRemove={() => removeItem('them', item.id)} />
                        ))}
                        <button
                            onClick={() => setSearchSide('them')}
                            className="w-24 h-28 md:w-32 md:h-36 border-2 border-dashed border-pink-300 rounded-2xl flex flex-col items-center justify-center text-pink-300 hover:text-pink-500 hover:border-pink-500 hover:bg-pink-50 transition-all group"
                        >
                            <div className="bg-pink-100 p-2 rounded-full mb-1 group-hover:scale-110 transition-transform">
                                <Plus size={24} className="text-pink-500" />
                            </div>
                            <span className="text-xs font-bold">Add Pet</span>
                        </button>
                    </div>
                </div>
            </div>

            {/* SEARCH MODAL */}
            <SearchModal
                isOpen={!!searchSide}
                onClose={() => setSearchSide(null)}
                side={searchSide ?? 'me'}
                onAddItem={handleAddItem}
            />

            <SettingsModal isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />
        </div>
    );
}
