import { useMemo } from 'react';
import { useTradeStore } from '../store/tradeStore';
import { motion } from 'framer-motion';

export function WinLoseBar() {
    const { myItems, theirItems } = useTradeStore();

    const myTotal = useMemo(() => myItems.reduce((acc, i) => acc + i.value, 0), [myItems]);
    const theirTotal = useMemo(() => theirItems.reduce((acc, i) => acc + i.value, 0), [theirItems]);

    const diff = theirTotal - myTotal;
    const isWin = diff > 0;
    const isFair = Math.abs(diff) < 0.1; // Tolerance for fairness

    // Calculate percentage for the bar shift (clamped)
    // Max shift at let's say 10 value difference for visual effect? Or relative?
    // Let's try relative to total value, or just a capped log scale for visual feedback
    // Standard simple linear representation: 
    const totalValue = myTotal + theirTotal || 1;
    const winPercentage = Math.min(Math.max((diff / totalValue) * 50, -50), 50);

    const getStatusColor = () => {
        if (isFair) return 'bg-game-fair text-gray-400';
        return isWin ? 'bg-game-win text-white' : 'bg-game-lose text-white';
    };

    const getStatusText = () => {
        if (isFair) return 'FAIR';
        return isWin ? 'WIN' : 'LOSE';
    };

    return (
        <div className="w-full max-w-2xl mx-auto px-4 py-2 flex flex-col items-center gap-2">
            {/* Status Badge */}
            <div className={`px-6 py-1 rounded-full font-bold text-lg shadow-md transition-colors duration-300 ${getStatusColor()}`}>
                {getStatusText()} {Math.abs(diff) > 0.01 && <span>({diff > 0 ? '+' : ''}{diff.toFixed(2)})</span>}
            </div>

            {/* Bar Container */}
            <div className="relative w-full h-4 bg-gray-300 rounded-full overflow-hidden shadow-inner">
                {/* Center Marker */}
                <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-gray-400 z-10 transform -translate-x-1/2"></div>

                {/* The gauge bar */}
                <motion.div
                    className={`absolute h-full ${isWin ? 'bg-game-win' : 'bg-game-lose'}`}
                    initial={{ width: 0, left: '50%' }}
                    animate={{
                        // If win, grow from 50% to right. If lose, grow from 50% to left.
                        left: isWin ? '50%' : `${50 + (winPercentage)}%`,
                        width: `${Math.abs(winPercentage)}%`
                    }}
                    transition={{ type: 'spring', stiffness: 100 }}
                />
            </div>
        </div>
    );
}
