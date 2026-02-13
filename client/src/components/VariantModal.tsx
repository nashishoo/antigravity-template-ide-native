import { X } from 'lucide-react';
import { useTradeStore, type TradeItem, type Variant, type Potion } from '../store/tradeStore';

interface VariantModalProps {
    item: TradeItem;
    side: 'me' | 'them';
    isOpen: boolean;
    onClose: () => void;
}

export function VariantModal({ item, side, isOpen, onClose }: VariantModalProps) {
    const { updateItem } = useTradeStore();

    if (!isOpen) return null;

    const handleVariantChange = (variant: Variant) => {
        // Toggle logic: If clicking the active variant, do nothing or user might expect deselect? 
        // Usually variant is a radio choice.
        if (item.variant === variant) return; // Already selected
        updateItem(side, item.id, { variant });
    };

    const togglePotion = (potion: Potion) => {
        const hasPotion = item.potions.includes(potion);
        let newPotions = [...item.potions];
        if (hasPotion) {
            newPotions = newPotions.filter(p => p !== potion);
        } else {
            newPotions.push(potion);
        }
        updateItem(side, item.id, { potions: newPotions });
    };

    return (
        <div className="fixed inset-0 z-[60] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl shadow-xl w-full max-w-sm overflow-hidden animate-in fade-in zoom-in duration-200">
                <div className="relative p-6 text-center">
                    <button onClick={onClose} className="absolute top-4 right-4 p-1 hover:bg-gray-100 rounded-full transition">
                        <X size={20} className="text-gray-500" />
                    </button>

                    <h3 className="text-xl font-bold text-gray-800 mb-1">{item.name}</h3>
                    <p className="text-sm text-gray-500 mb-6">Customize Item</p>

                    {/* Potions */}
                    <div className="mb-6">
                        <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Potions</h4>
                        <div className="flex justify-center gap-4">
                            <button
                                onClick={() => togglePotion('Fly')}
                                className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg transition-all border-2 ${item.potions.includes('Fly')
                                    ? 'bg-blue-100 border-game-badge-fly text-game-badge-fly shadow-[0_0_10px_rgba(59,130,246,0.5)]'
                                    : 'bg-gray-100 border-gray-200 text-gray-400'
                                    }`}
                            >
                                F
                            </button>
                            <button
                                onClick={() => togglePotion('Ride')}
                                className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg transition-all border-2 ${item.potions.includes('Ride')
                                    ? 'bg-pink-100 border-game-badge-ride text-game-badge-ride shadow-[0_0_10px_rgba(236,72,153,0.5)]'
                                    : 'bg-gray-100 border-gray-200 text-gray-400'
                                    }`}
                            >
                                R
                            </button>
                        </div>
                    </div>

                    {/* Variants */}
                    <div>
                        <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Variants</h4>
                        <div className="flex justify-center gap-3">
                            {/* Regular */}
                            <button
                                onClick={() => handleVariantChange('Regular')}
                                className={`px-4 py-2 rounded-lg font-bold text-sm transition-all border-2 ${item.variant === 'Regular'
                                    ? 'bg-gray-800 border-gray-800 text-white'
                                    : 'bg-white border-gray-200 text-gray-500 hover:border-gray-300'
                                    }`}
                            >
                                Regular
                            </button>

                            {/* Neon */}
                            <button
                                onClick={() => handleVariantChange('Neon')}
                                className={`px-4 py-2 rounded-lg font-bold text-sm transition-all border-2 ${item.variant === 'Neon'
                                    ? 'bg-green-100 border-game-badge-neon text-game-badge-neon shadow-[0_0_10px_rgba(132,204,22,0.4)]'
                                    : 'bg-white border-gray-200 text-gray-500 hover:border-gray-300'
                                    }`}
                            >
                                Neon
                            </button>

                            {/* Mega */}
                            <button
                                onClick={() => handleVariantChange('Mega')}
                                className={`px-4 py-2 rounded-lg font-bold text-sm transition-all border-2 ${item.variant === 'Mega'
                                    ? 'bg-purple-100 border-game-badge-mega text-game-badge-mega shadow-[0_0_10px_rgba(168,85,247,0.4)]'
                                    : 'bg-white border-gray-200 text-gray-500 hover:border-gray-300'
                                    }`}
                            >
                                Mega
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
