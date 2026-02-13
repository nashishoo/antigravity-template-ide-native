import { useState, useEffect } from 'react';
import { useTradeStore } from '../store/tradeStore';
import { Sparkles, Brain, X, Scan } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface AnalysisResult {
    score: number;
    verdict: string;
    comment: string;
    tip: string;
}

export const AIAdvisor = () => {
    const { myItems, theirItems } = useTradeStore();
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [isOpen, setIsOpen] = useState(false);
    const [hasNewChanges, setHasNewChanges] = useState(false);

    useEffect(() => {
        if (myItems.length > 0 || theirItems.length > 0) {
            setHasNewChanges(true);
        }
    }, [myItems, theirItems]);

    const handleAnalyze = async () => {
        setHasNewChanges(false);
        setIsOpen(true);
        setLoading(true);
        setResult(null);

        try {
            const response = await fetch('http://localhost:3000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ myItems, theirItems }),
            });

            if (!response.ok) throw new Error('Analysis failed');

            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error('Error:', error);
            // Fallback for demo/error
            setResult({
                score: 0,
                verdict: 'ERROR',
                comment: 'My circuits are fried! Check the connection.',
                tip: 'Try again later.',
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed bottom-4 right-4 z-50">
            {/* Trigger Button */}
            {!isOpen && (
                <motion.button
                    onClick={handleAnalyze}
                    className={`relative group flex items-center gap-2 px-6 py-3 rounded-full font-bold text-white shadow-lg transition-all
                    ${hasNewChanges ? 'bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:scale-105' : 'bg-gray-800 hover:bg-gray-700'}
                    `}
                    animate={hasNewChanges ? {
                        boxShadow: ["0 0 0 0px rgba(139, 92, 246, 0.5)", "0 0 0 4px rgba(139, 92, 246, 0)"],
                    } : {}}
                    transition={hasNewChanges ? {
                        duration: 1.5,
                        repeat: Infinity,
                    } : {}}
                >
                    <Sparkles className={`w-5 h-5 ${hasNewChanges ? 'animate-spin-slow' : ''}`} />
                    <span>Ask Gemini</span>
                    {hasNewChanges && (
                        <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-ping" />
                    )}
                </motion.button>
            )}

            {/* Holographic Panel */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.8, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.8, y: 20 }}
                        className="relative w-80 md:w-96 bg-black/80 backdrop-blur-xl border border-violet-500/50 rounded-2xl overflow-hidden shadow-2xl shadow-violet-500/20"
                    >
                        {/* Header */}
                        <div className="flex items-center justify-between p-4 border-b border-violet-500/30 bg-violet-900/20">
                            <div className="flex items-center gap-2 text-violet-300">
                                <Brain className="w-5 h-5" />
                                <span className="font-mono text-sm tracking-wider uppercase">Advisor.AI</span>
                            </div>
                            <button
                                onClick={() => setIsOpen(false)}
                                className="text-gray-400 hover:text-white transition-colors"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>

                        {/* Content */}
                        <div className="p-6 min-h-[300px] flex flex-col items-center justify-center text-center relative">
                            {/* Scanning Effect Overlay */}
                            <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(18,16,23,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] z-0 bg-[length:100%_4px,3px_100%]" />

                            {loading ? (
                                <div className="space-y-4 z-10">
                                    <Scan className="w-12 h-12 text-violet-400 animate-pulse mx-auto" />
                                    <p className="text-violet-200 font-mono text-sm animate-pulse">Analyzing market data...</p>
                                </div>
                            ) : result ? (
                                <div className="w-full space-y-4 z-10 text-left">
                                    <div className="flex items-center justify-between">
                                        <div className={`text-2xl font-black italic tracking-tighter
                                            ${result.verdict.includes('WIN') ? 'text-green-400 drop-shadow-[0_0_10px_rgba(74,222,128,0.5)]' :
                                                result.verdict.includes('LOSE') ? 'text-red-400 drop-shadow-[0_0_10px_rgba(248,113,113,0.5)]' : 'text-yellow-400'
                                            }`}>
                                            {result.verdict}
                                        </div>
                                        <div className="flex items-center gap-1">
                                            <span className="text-4xl font-bold text-white">{result.score}</span>
                                            <span className="text-sm text-gray-400">/10</span>
                                        </div>
                                    </div>

                                    <div className="h-px w-full bg-gradient-to-r from-transparent via-violet-500/50 to-transparent" />

                                    <div className="space-y-2">
                                        <p className="text-gray-200 text-sm leading-relaxed font-medium">
                                            "{result.comment}"
                                        </p>
                                        <div className="bg-violet-900/30 border border-violet-500/30 p-3 rounded-lg mt-4">
                                            <div className="flex items-center gap-2 text-xs font-bold text-violet-300 uppercase mb-1">
                                                <Sparkles className="w-3 h-3" />
                                                Negotiation Tip
                                            </div>
                                            <p className="text-violet-100 text-xs italic">
                                                {result.tip}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            ) : null}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};
