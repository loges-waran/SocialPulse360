import React from 'react';
import { ShieldCheck, HardHat, Globe, Factory } from 'lucide-react';

export default function SDG9Badge() {
  return (
    <div className="p-4 rounded-xl glass-panel border border-orange-500/30 bg-gradient-to-br from-orange-950/20 via-gray-900/60 to-gray-950 shadow-lg">
      <div className="flex items-start space-x-3">
        <div className="p-2.5 rounded-lg bg-orange-600/20 border border-orange-500/40 text-orange-400 shrink-0">
          <Factory className="w-5 h-5" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold uppercase tracking-wider text-orange-400">
              UN Sustainable Development Goal 9
            </span>
            <span className="text-[10px] font-semibold bg-orange-950 text-orange-300 border border-orange-800/80 px-2 py-0.5 rounded-full">
              Industry, Innovation & Infrastructure
            </span>
          </div>
          <p className="mt-1 text-xs text-gray-300 leading-relaxed">
            SocialPulse 360 supports <strong>SDG Target 9.1 & 9.c</strong> by providing real-time citizen sentiment and public infrastructure feedback across digital communications, transport transit networks (rail/metro/highways), smart cities, and industrial innovation corridors.
          </p>
        </div>
      </div>
    </div>
  );
}
