import { X } from 'lucide-react';
import { useTradeStore } from '../store/tradeStore';

export function SettingsModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
    const { showDemand, toggleDemand } = useTradeStore();

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[60] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl shadow-xl w-full max-w-sm overflow-hidden">
                {/* Header */}
                <div className="bg-gray-100 p-4 border-b flex justify-between items-center">
                    <h3 className="font-bold text-lg text-gray-800">Settings</h3>
                    <button onClick={onClose} className="p-1 hover:bg-gray-200 rounded-full transition">
                        <X size={20} className="text-gray-500" />
                    </button>
                </div>

                {/* Content */}
                <div className="p-6">
                    <div className="flex items-center justify-between">
                        <div className="flex flex-col">
                            <span className="font-semibold text-gray-700">Show Demand</span>
                            <span className="text-xs text-gray-500">Display popularity stars on items</span>
                        </div>

                        <button
                            onClick={toggleDemand}
                            className={`w-12 h-6 rounded-full relative transition-colors duration-300 ${showDemand ? 'bg-game-win' : 'bg-gray-300'}`}
                        >
                            <div
                                className={`absolute top-1 w-4 h-4 rounded-full bg-white shadow-sm transition-all duration-300 ${showDemand ? 'left-7' : 'left-1'}`}
                            />
                        </button>
                    </div>
                </div>

                {/* Footer */}
                <div className="bg-gray-50 p-4 border-t text-center">
                    <button onClick={onClose} className="text-game-button font-bold text-sm hover:underline">Close</button>
                </div>
            </div>
        </div>
    );
}
