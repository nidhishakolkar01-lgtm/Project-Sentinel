import React, { useState, useEffect } from 'react';
import { Shield, Navigation, Video, Database, Activity, Layers } from 'lucide-react';
import GISMap from './components/GISMap';
import RouteTracer from './components/RouteTracer';
import VideoWall from './components/VideoWall';
import CameraRegistry from './components/CameraRegistry';
import AlertBanner from './components/AlertBanner';
import { fetchCameras, fetchDetections } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('map'); // 'map', 'route', 'videowall', 'registry'
  const [cameras, setCameras] = useState([]);
  const [selectedCamera, setSelectedCamera] = useState(null);
  const [alertCameraId, setAlertCameraId] = useState(null);
  const [activeRoutePoints, setActiveRoutePoints] = useState(null);
  const [activeAlert, setActiveAlert] = useState(null);
  const [recentDetections, setRecentDetections] = useState([]);

  // Load Initial Camera Inventory & Detections
  const loadData = async () => {
    const cams = await fetchCameras();
    setCameras(cams);
    const dets = await fetchDetections();
    setRecentDetections(dets);
  };

  useEffect(() => {
    loadData();

    // Auto-Reconnecting WebSocket Alert Gateway
    let socket = null;
    let reconnectTimeout = null;

    const connectWebSocket = () => {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = window.location.host;
      const wsUrl = `${protocol}//${host}/ws/alerts`;
      
      socket = new WebSocket(wsUrl);

      socket.onmessage = (event) => {
        try {
          const alertObj = JSON.parse(event.data);
          if (alertObj.event_type === 'WATCHLIST_MATCH_ALERT') {
            setActiveAlert(alertObj);
            if (alertObj.data && alertObj.data.camera_code) {
              setAlertCameraId(alertObj.data.camera_code);
            }
          }
        } catch (e) {
          console.warn("WebSocket message parse notice", e);
        }
      };

      socket.onclose = () => {
        // Reconnect after 3 seconds if disconnected
        reconnectTimeout = setTimeout(connectWebSocket, 3000);
      };

      socket.onerror = () => {
        socket.close();
      };
    };

    connectWebSocket();

    return () => {
      if (socket) socket.close();
      if (reconnectTimeout) clearTimeout(reconnectTimeout);
    };
  }, []);

  const handleSelectCamera = (cam) => {
    setSelectedCamera(cam);
    setActiveTab('videowall');
  };

  const handleAlertViewOnMap = (alertData) => {
    setAlertCameraId(alertData.camera_code);
    setActiveTab('map');
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
      {/* Top Header Bar */}
      <header className="h-16 bg-slate-900/90 border-b border-slate-800 px-6 flex items-center justify-between z-50 shrink-0 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-600/20 border border-cyan-500/40 flex items-center justify-center text-cyan-400 shadow-lg shadow-cyan-950">
            <Shield size={22} />
          </div>
          <div>
            <h1 className="text-base font-extrabold text-white tracking-wide flex items-center gap-2">
              PROJECT SENTINEL
              <span className="text-[10px] bg-cyan-950 text-cyan-400 border border-cyan-800 px-2 py-0.5 rounded font-mono">
                MODEL 5 HYBRID ARCHITECTURE
              </span>
            </h1>
            <p className="text-[11px] text-slate-400 font-medium">
              Gujarat Police CCTV Integration Platform — 26 Government Departments (~80,000 Cameras)
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex gap-1.5 bg-slate-950 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab('map')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition flex items-center gap-1.5 ${activeTab === 'map' ? 'bg-cyan-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <Layers size={14} /> GIS Interactive Map
          </button>
          <button
            onClick={() => setActiveTab('route')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition flex items-center gap-1.5 ${activeTab === 'route' ? 'bg-cyan-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <Navigation size={14} /> Step 4 Route Tracer
          </button>
          <button
            onClick={() => setActiveTab('videowall')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition flex items-center gap-1.5 ${activeTab === 'videowall' ? 'bg-cyan-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <Video size={14} /> Video Wall Grid
          </button>
          <button
            onClick={() => setActiveTab('registry')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition flex items-center gap-1.5 ${activeTab === 'registry' ? 'bg-cyan-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <Database size={14} /> Asset Registry (Model 1)
          </button>
        </nav>
      </header>

      {/* Main Content Viewport */}
      <main className="flex-1 p-4 overflow-hidden relative">
        {/* Real-Time Watchlist Match Alert Banner */}
        <AlertBanner
          alert={activeAlert}
          onClose={() => setActiveAlert(null)}
          onViewOnMap={handleAlertViewOnMap}
        />

        {/* Tab 1: GIS Interactive Map View */}
        {activeTab === 'map' && (
          <div className="w-full h-full flex gap-4">
            <div className="flex-1 h-full">
              <GISMap
                cameras={cameras}
                alertCameraId={alertCameraId}
                routePoints={activeRoutePoints}
                onSelectCamera={handleSelectCamera}
              />
            </div>
            
            {/* Quick Activity Sidebar */}
            <div className="w-80 h-full bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col gap-3 shrink-0 shadow-2xl overflow-y-auto">
              <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                <Activity size={14} className="text-cyan-400" /> Real-Time ANPR Feed
              </h3>
              <div className="flex flex-col gap-2">
                {recentDetections.map((d) => (
                  <div key={d.id} className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 text-xs">
                    <div className="flex items-center justify-between">
                      <span className="font-mono font-bold text-amber-400">{d.detected_plate}</span>
                      <span className="text-[10px] text-slate-400">{new Date(d.detected_at).toLocaleTimeString()}</span>
                    </div>
                    <p className="text-[11px] text-slate-300 mt-1">{d.location_name}</p>
                    {d.is_watchlist_hit && (
                      <span className="mt-1 inline-block bg-red-950 text-red-400 border border-red-800 px-1.5 py-0.5 rounded text-[9px] font-bold">
                        ⚠️ WATCHLIST HIT ({d.watchlist_category})
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: Step 4 Route Tracer View */}
        {activeTab === 'route' && (
          <div className="w-full h-full flex gap-4">
            <div className="w-96 h-full shrink-0">
              <RouteTracer onRouteLoaded={(pts) => setActiveRoutePoints(pts)} />
            </div>
            <div className="flex-1 h-full">
              <GISMap
                cameras={cameras}
                alertCameraId={alertCameraId}
                routePoints={activeRoutePoints}
                onSelectCamera={handleSelectCamera}
              />
            </div>
          </div>
        )}

        {/* Tab 3: Video Wall Grid View */}
        {activeTab === 'videowall' && (
          <div className="w-full h-full">
            <VideoWall cameras={cameras} selectedCamera={selectedCamera} />
          </div>
        )}

        {/* Tab 4: Model 1 Asset Registry View */}
        {activeTab === 'registry' && (
          <div className="w-full h-full">
            <CameraRegistry cameras={cameras} onRefresh={loadData} />
          </div>
        )}
      </main>
    </div>
  );
}
