import React, { useState } from 'react';
import { Search, Navigation, Clock, MapPin, ShieldAlert, CheckCircle2, ArrowRight } from 'lucide-react';
import { fetchVehicleRoute } from '../services/api';

export default function RouteTracer({ onRouteLoaded }) {
  const [plateInput, setPlateInput] = useState('GJ01HK9988');
  const [loading, setLoading] = useState(false);
  const [routeData, setRouteData] = useState(null);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    if (!plateInput.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const res = await fetchVehicleRoute(plateInput.trim());
      setRouteData(res);
      if (onRouteLoaded) {
        onRouteLoaded(res.trajectory);
      }
    } catch (err) {
      setError(`No vehicle trajectory found for '${plateInput}'. Try 'GJ01HK9988'.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-2xl flex flex-col gap-4 h-full overflow-y-auto">
      {/* Header Banner */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Navigation className="text-cyan-400" size={18} />
            Step 4 Challenge: Vehicle Route Trajectory Engine
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Trace target vehicle movement chronologically across Gujarat CCTV GIS map
          </p>
        </div>
        <span className="px-2.5 py-1 bg-cyan-950 text-cyan-300 border border-cyan-800 text-[11px] font-bold rounded-lg">
          Live Evaluation Mode
        </span>
      </div>

      {/* Search Input Box */}
      <form onSubmit={handleSearch} className="flex gap-2">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-2.5 text-slate-400" size={16} />
          <input
            type="text"
            value={plateInput}
            onChange={(e) => setPlateInput(e.target.value)}
            placeholder="Enter Plate (e.g. GJ01HK9988)"
            className="w-full bg-slate-950 border border-slate-700 text-slate-100 placeholder-slate-500 rounded-xl pl-9 pr-4 py-2 text-sm font-mono font-semibold focus:outline-none focus:border-cyan-500 transition"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 disabled:bg-slate-700 text-white font-medium text-xs rounded-xl shadow transition flex items-center gap-1.5"
        >
          {loading ? 'Tracing...' : 'Trace Trajectory'}
        </button>
      </form>

      {/* Error Banner */}
      {error && (
        <div className="p-3 bg-red-950/80 border border-red-800 rounded-xl text-red-300 text-xs flex items-center gap-2">
          <ShieldAlert size={16} />
          {error}
        </div>
      )}

      {/* Trajectory Results Display */}
      {routeData && (
        <div className="flex flex-col gap-4 mt-1">
          {/* Summary Metric Badges */}
          <div className="grid grid-cols-3 gap-2 text-center">
            <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
              <span className="text-[10px] text-slate-400 uppercase font-semibold block">Target Vehicle</span>
              <span className="text-sm font-bold text-cyan-400 font-mono">{routeData.target_plate}</span>
            </div>
            <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
              <span className="text-[10px] text-slate-400 uppercase font-semibold block">Checkpoints</span>
              <span className="text-sm font-bold text-emerald-400">{routeData.total_checkpoints} Cameras</span>
            </div>
            <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
              <span className="text-[10px] text-slate-400 uppercase font-semibold block">Total Distance</span>
              <span className="text-sm font-bold text-amber-400">{routeData.total_distance_km} km</span>
            </div>
          </div>

          {/* Chronological Checkpoint Timeline */}
          <div className="flex flex-col gap-2.5">
            <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
              Chronological Path Checkpoints
            </h3>
            {routeData.trajectory.map((pt, idx) => (
              <div
                key={pt.sequence}
                className="bg-slate-950/80 border border-slate-800 hover:border-cyan-800 p-3 rounded-xl flex items-start gap-3 transition"
              >
                <div className="w-7 h-7 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-700 flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                  {pt.sequence}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-bold text-sm text-slate-200 truncate">{pt.location_name}</span>
                    <span className="text-[10px] font-mono text-cyan-400 bg-slate-900 px-2 py-0.5 rounded">
                      {pt.camera_code}
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-xs text-slate-400 mt-1">
                    <span className="flex items-center gap-1">
                      <Clock size={12} className="text-slate-500" />
                      {new Date(pt.timestamp).toLocaleTimeString()}
                    </span>
                    <span className="flex items-center gap-1">
                      <MapPin size={12} className="text-slate-500" />
                      {pt.district}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
