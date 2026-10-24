import React, { useEffect } from 'react';
import { ShieldAlert, X, AlertTriangle, Video } from 'lucide-react';

export default function AlertBanner({ alert, onClose, onViewOnMap }) {
  useEffect(() => {
    if (alert) {
      // Play 880Hz Emergency Chime Sound via Web Audio API
      try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(880, audioCtx.currentTime); // 880Hz High Emergency Pitch
        gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.6);
      } catch (e) {
        console.warn("Audio Context blocked by browser policy");
      }
    }
  }, [alert]);

  if (!alert) return null;

  const data = alert.data || alert;

  return (
    <div className="fixed top-5 right-5 z-[9999] max-w-md w-full bg-red-950/95 border-2 border-red-500 rounded-2xl shadow-2xl p-4 text-slate-100 backdrop-blur-xl animate-bounce">
      <div className="flex items-start justify-between gap-3">
        <div className="p-2 rounded-xl bg-red-900/80 text-red-200 shrink-0">
          <ShieldAlert size={24} />
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <span className="bg-red-600 text-white font-extrabold text-[10px] uppercase px-2 py-0.5 rounded tracking-wide">
              {data.severity || 'CRITICAL'} WATCHLIST MATCH
            </span>
            <span className="text-xs text-red-200 font-mono">{new Date(data.timestamp || Date.now()).toLocaleTimeString()}</span>
          </div>
          <h3 className="text-base font-extrabold text-white mt-1 font-mono">
            Target Plate: <span className="text-amber-300 underline">{data.detected_plate}</span>
          </h3>
          <p className="text-xs text-red-200 mt-0.5">
            Location: <span className="font-semibold text-white">{data.location_name || data.camera_code}</span>
          </p>
          <p className="text-[11px] text-red-300 mt-1 font-medium">
            Category: {data.watchlist_category || 'Stolen Vehicle / FIR Alert'}
          </p>

          <div className="flex gap-2 mt-3">
            <button
              onClick={() => onViewOnMap(data)}
              className="px-3 py-1.5 bg-red-600 hover:bg-red-500 text-white text-xs font-bold rounded-lg shadow transition flex items-center gap-1"
            >
              <Video size={14} /> Highlight on GIS Map
            </button>
            <button
              onClick={onClose}
              className="px-3 py-1.5 bg-red-900/60 hover:bg-red-900 text-red-200 text-xs font-medium rounded-lg transition"
            >
              Dismiss
            </button>
          </div>
        </div>
        <button onClick={onClose} className="text-red-400 hover:text-white p-1">
          <X size={18} />
        </button>
      </div>
    </div>
  );
}
