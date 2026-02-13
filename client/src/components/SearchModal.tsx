import { useState } from 'react';
import { Search, X } from 'lucide-react';
import { useSearch, type SourceItem } from '../hooks/useSearch';

interface SearchModalProps {
    isOpen: boolean;
    onClose: () => void;
    side: 'me' | 'them';
    onAddItem: (item: SourceItem) => void;
}

export function SearchModal({ isOpen, onClose, side, onAddItem }: SearchModalProps) {
    const [searchTerm, setSearchTerm] = useState('');
    const filteredItems = useSearch(searchTerm);

    if (!isOpen) return null;

    const handleSelect = (item: SourceItem) => {
        onAddItem(item);
        setSearchTerm('');
        onClose();
    };

    return (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-start justify-center pt-20 animate-in fade-in duration-200">
            <div className="w-11/12 max-w-lg bg-white rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[80vh]">
                <div className="p-4 border-b border-gray-100 flex gap-2 items-center">
                    <div className="relative flex-1">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                        <input
                            type="text"
                            placeholder={`Search pets for ${side === 'me' ? 'your' : 'their'} offer...`}
                            autoFocus
                            className="w-full bg-gray-100 border-transparent rounded-xl pl-10 pr-4 py-3 text-gray-800 placeholder-gray-400 focus:bg-white focus:ring-2 focus:ring-game-button focus:outline-none transition-all"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-gray-100 rounded-full text-gray-500 transition"
                    >
                        <X size={24} />
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto p-2">
                    <div className="flex flex-col gap-1">
                        {filteredItems.map((item, index) => (
                            <div
                                key={item.name + index}
                                onClick={() => handleSelect(item)}
                                className="flex items-center gap-4 p-3 hover:bg-blue-50 rounded-xl cursor-pointer transition-colors group"
                            >
                                <div className="w-12 h-12 bg-white rounded-lg shadow-sm border border-gray-100 p-1 flex items-center justify-center group-hover:scale-105 transition-transform">
                                    <img src={item.image_url} alt={item.name} className="max-w-full max-h-full object-contain" />
                                </div>
                                <div>
                                    <div className="font-bold text-gray-800">{item.name}</div>
                                    <div className="text-xs font-medium text-gray-400">Value: {item.base_value}</div>
                                </div>
                            </div>
                        ))}
                    </div>

                    {searchTerm && filteredItems.length === 0 && (
                        <div className="text-center text-gray-400 py-10 flex flex-col items-center">
                            <Search size={40} className="mb-2 opacity-20" />
                            <p>No pets found matching "{searchTerm}"</p>
                        </div>
                    )}
                    {!searchTerm && (
                        <div className="text-center text-gray-400 py-10">
                            <p>Type to search...</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
