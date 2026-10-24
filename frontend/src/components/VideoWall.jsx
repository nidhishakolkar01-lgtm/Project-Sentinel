import React, { useState } from 'react';
import { Grid, Video, Play, Maximize2 } from 'lucide-react';

export default function VideoWall({ cameras, selectedCamera }) {
  const [gridSize, setGridSize] = useState(4); // 2x2 grid by default
  const activeCams = cameras.slice(0, gridSize);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-2xl flex flex-col gap-4 h-full">
      {/* Header Controls */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Video className="text-cyan-400" size={18} />
            Model 2: Unified Command Center Video Wall
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            On-Demand WebRTC & RTSP Multi-Camera Live Aggregation Grid
          </p>
        </div>

        {/* Grid Selector Buttons */}
        <div className="flex gap-1.5 bg-slate-950 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setGridSize(4)}
            className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition ${gridSize === 4 ? 'bg-cyan-600 text-white' : 'text-slate-400 hover:text-white'}`}
          >
            2x2 Grid
          </button>
          <button
            onClick={() => setGridSize(9)}
            className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition ${gridSize === 9 ? 'bg-cyan-600 text-white' : 'text-slate-400 hover:text-white'}`}
          >
            3x3 Grid
          </button>
        </div>
      </div>

      {/* Camera Video Grid */}
      <div className={`grid gap-3 flex-1 ${gridSize === 4 ? 'grid-cols-2 grid-rows-2' : 'grid-cols-3 grid-rows-3'}`}>
        {activeCams.map((cam) => {
          const isTarget = selectedCamera && selectedCamera.id === cam.id;
          return (
            <div
              key={cam.id || cam.camera_code}
              className={`relative bg-slate-950 rounded-xl overflow-hidden border ${isTarget ? 'border-cyan-500 ring-2 ring-cyan-500/50' : 'border-slate-800'} flex flex-col justify-between p-3`}
            >
              {/* Simulated Live Stream Overlay */}
              <div className="absolute inset-0 bg-slate-900/90 flex flex-col items-center justify-center p-4 text-center">
                <div className="w-12 h-12 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-cyan-400 mb-2">
                  <Play size={20} className="ml-0.5" />
                </div>
                <span className="text-xs font-bold text-slate-200">{cam.camera_code}</span>
                <span className="text-[10px] text-slate-400 truncate max-w-full">{cam.installation_address}</span>
                <span className="mt-2 text-[9px] font-mono bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded">
                  WebRTC Live Stream (Sub-300ms)
                </span>
              </div>

              {/* Camera Metadata Overlay Header */}
              <div className="relative z-10 flex items-center justify-between">
                <span className="bg-slate-950/80 px-2 py-0.5 rounded text-[10px] font-bold text-cyan-400 border border-slate-800">
                  {cam.camera_code}
                </span>
                <span className="bg-emerald-950/80 text-emerald-400 border border-emerald-800 px-1.5 py-0.5 rounded text-[9px] font-bold">
                  ● LIVE
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
