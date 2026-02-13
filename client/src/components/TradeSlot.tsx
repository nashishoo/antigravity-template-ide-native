import { useState } from 'react';
import { motion } from 'framer-motion';
import { X, Star } from 'lucide-react';
import { useTradeStore, type TradeItem } from '../store/tradeStore';
import { VariantModal } from './VariantModal';

interface TradeSlotProps {
    item: TradeItem;
    side: 'me' | 'them';
    onRemove?: () => void;
}

export function TradeSlot({ item, side, onRemove }: TradeSlotProps) {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const { showDemand } = useTradeStore();

    const getBorderColor = () => {
        if (item.variant === 'Mega') return 'border-game-badge-mega shadow-[0_0_8px_rgba(168,85,247,0.4)]';
        if (item.variant === 'Neon') return 'border-game-badge-neon shadow-[0_0_8px_rgba(132,204,22,0.4)]';
        return 'border-gray-200';
    };

    return (
        <>
            <motion.div
                layout
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.8, opacity: 0 }}
                onClick={() => setIsModalOpen(true)}
                className={`relative w-24 h-28 md:w-32 md:h-36 bg-game-card border-2 rounded-2xl flex flex-col items-center cursor-pointer hover:-translate-y-1 transition-all ${getBorderColor()}`}
            >
                {onRemove && (
                    <button
                        onClick={(e) => { e.stopPropagation(); onRemove(); }}
                        className="absolute -top-2 -right-2 p-1.5 bg-game-lose text-white rounded-full shadow-md z-10 hover:scale-110 transition"
                    >
                        <X size={12} strokeWidth={3} />
                    </button>
                )}

                {/* Demand Stars */}
                {showDemand && item.demand && (
                    <div className="absolute top-1 left-1 flex gap-0.5 z-10">
                        {Array.from({ length: item.demand }).map((_, i) => (
                            <Star key={i} size={10} className="fill-yellow-400 text-yellow-400" />
                        ))}
                    </div>
                )}

                {/* Image Area */}
                <div className="flex-1 w-full p-2 flex items-center justify-center relative">
                    <img src={item.image} alt={item.name} className="max-w-full max-h-full object-contain drop-shadow-sm" />

                    {/* Potion Badges */}
                    <div className="absolute bottom-0 right-1 flex gap-1">
                        {item.potions.includes('Fly') && (
                            <span className="bg-game-badge-fly text-white text-[9px] font-bold px-1 rounded-sm shadow-sm">F</span>
                        )}
                        {item.potions.includes('Ride') && (
                            <span className="bg-game-badge-ride text-white text-[9px] font-bold px-1 rounded-sm shadow-sm">R</span>
                        )}
                    </div>
                </div>

                {/* Name and Variant Label */}
                <div className="w-full bg-game-cardDark/50 p-1.5 rounded-b-xl text-center">
                    <div className="text-[10px] md:text-xs font-bold truncate text-gray-700">{item.name}</div>
                    {(item.variant === 'Neon' || item.variant === 'Mega') && (
                        <div className={`text-[9px] font-extrabold uppercase ${item.variant === 'Neon' ? 'text-game-badge-neon' : 'text-game-badge-mega'}`}>
                            {item.variant}
                        </div>
                    )}
                </div>
            </motion.div>

            <VariantModal
                item={item}
                side={side}
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
            />
        </>
    );
}
