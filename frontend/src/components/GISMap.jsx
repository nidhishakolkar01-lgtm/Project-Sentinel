import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, Tooltip, useMap } from 'react-leaflet';
import L from 'leaflet';
import { Video, ShieldAlert, CheckCircle2, AlertTriangle } from 'lucide-react';

// Custom Leaflet Icons for Cameras
const createCameraIcon = (status, isAlert) => {
  let colorClass = 'bg-emerald-500 text-emerald-950 border-emerald-300';
  if (status === 'OFFLINE') colorClass = 'bg-slate-600 text-slate-200 border-slate-400';
  if (isAlert) colorClass = 'bg-red-600 text-white border-red-300 beacon-red';

  return L.divIcon({
    className: 'custom-leaflet-marker',
    html: `<div class="w-8 h-8 rounded-full flex items-center justify-center border-2 shadow-lg ${colorClass} transition-all duration-300 transform hover:scale-125">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m22 8-6 4 6 4V8Z"/><rect width="14" height="12" x="2" y="6" rx="2" ry="2"/></svg>
    </div>`,
    iconSize: [32, 32],
    iconAnchor: [16, 16]
  });
};

const createRouteIcon = (seq) => {
  return L.divIcon({
    className: 'custom-route-marker',
    html: `<div class="w-7 h-7 rounded-full bg-cyan-500 text-slate-950 font-bold text-xs flex items-center justify-center border-2 border-white shadow-xl">
      ${seq}
    </div>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14]
  });
};

function ChangeMapView({ center, zoom }) {
  const map = useMap();
  useEffect(() => {
    if (center) {
      map.setView(center, zoom);
    }
  }, [center, zoom, map]);
  return null;
}

export default function GISMap({ cameras, alertCameraId, routePoints, onSelectCamera }) {
  const gujaratCenter = [22.75, 72.00]; // Gujarat Center Lat/Lng
  
  // Calculate Polyline Coordinates for Route Trajectory
  const polylineCoords = routePoints ? routePoints.map(p => [p.latitude, p.longitude]) : [];

  return (
    <div className="relative w-full h-full rounded-2xl overflow-hidden border border-slate-800 shadow-2xl">
      <MapContainer center={gujaratCenter} zoom={8} scrollWheelZoom={true} className="w-full h-full">
        <ChangeMapView center={polylineCoords.length > 0 ? polylineCoords[polylineCoords.length - 1] : null} zoom={polylineCoords.length > 0 ? 10 : 8} />
        
        {/* Dark Map Tiles */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
        />

        {/* Render 50 Cameras */}
        {cameras.map((cam) => {
          const isAlert = cam.id === alertCameraId || cam.camera_code === alertCameraId;
          return (
            <Marker
              key={cam.id || cam.camera_code}
              position={[cam.latitude, cam.longitude]}
              icon={createCameraIcon(cam.status, isAlert)}
              eventHandlers={{
                click: () => onSelectCamera(cam)
              }}
            >
              <Popup className="custom-leaflet-popup">
                <div className="p-3 bg-slate-900 text-slate-100 rounded-lg shadow-xl border border-slate-700 min-w-[220px]">
                  <div className="flex items-center justify-between gap-2 mb-2 pb-2 border-b border-slate-800">
                    <span className="font-bold text-cyan-400 text-sm tracking-wide">{cam.camera_code}</span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${cam.status === 'ONLINE' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-slate-800 text-slate-400'}`}>
                      {cam.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 font-medium mb-1">{cam.installation_address}</p>
                  <p className="text-[11px] text-slate-400 mb-2">Dept: <span className="text-slate-200">{cam.department_name}</span></p>
                  <div className="flex gap-2 text-[10px] text-slate-400 mb-3">
                    <span className="bg-slate-800 px-1.5 py-0.5 rounded">Vendor: {cam.vendor_name}</span>
                    <span className="bg-slate-800 px-1.5 py-0.5 rounded">District: {cam.district}</span>
                  </div>
                  <button
                    onClick={() => onSelectCamera(cam)}
                    className="w-full py-1.5 px-3 bg-cyan-600 hover:bg-cyan-500 text-white font-medium text-xs rounded transition flex items-center justify-center gap-1.5 shadow"
                  >
                    <Video size={14} /> View Live Stream
                  </button>
                </div>
              </Popup>
            </Marker>
          );
        })}

        {/* Step 4 Challenge: Draw Chronological Trajectory Route Polyline */}
        {polylineCoords.length > 0 && (
          <>
            <Polyline
              positions={polylineCoords}
              color="#06b6d4"
              weight={5}
              opacity={0.9}
              dashArray="8, 12"
            />
            {routePoints.map((pt) => (
              <Marker
                key={`route-${pt.sequence}`}
                position={[pt.latitude, pt.longitude]}
                icon={createRouteIcon(pt.sequence)}
              >
                <Tooltip permanent direction="top" offset={[0, -10]}>
                  <div className="bg-slate-950 text-slate-100 px-2 py-1 rounded border border-cyan-500 text-[11px] font-bold">
                    #{pt.sequence} {pt.camera_code} ({new Date(pt.timestamp).toLocaleTimeString()})
                  </div>
                </Tooltip>
              </Marker>
            ))}
          </>
        )}
      </MapContainer>

      {/* Map Control Overlay Banner */}
      <div className="absolute top-4 left-4 z-[1000] glass-panel px-4 py-2.5 rounded-xl shadow-lg flex items-center gap-3 text-xs font-semibold text-slate-200">
        <span className="flex items-center gap-1.5 text-emerald-400">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
          50 Active Multi-Vendor Cameras
        </span>
        <span className="text-slate-600">|</span>
        <span className="text-cyan-400">Model 1 GIS Asset Layer</span>
      </div>
    </div>
  );
}
