import React, { useState } from 'react';
import { Database, Plus, Search, Filter, CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';
import { onboardCamera } from '../services/api';

export default function CameraRegistry({ cameras, onRefresh }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [deptFilter, setDeptFilter] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);

  // Form State
  const [formData, setFormData] = useState({
    camera_code: '',
    department_name: 'Home Department / Gujarat Police',
    vendor_name: 'Hikvision',
    rtsp_url: '',
    latitude: 23.02,
    longitude: 72.57,
    district: 'Ahmedabad',
    installation_address: ''
  });

  const filteredCams = cameras.filter(c => {
    const matchSearch = c.camera_code.toLowerCase().includes(searchTerm.toLowerCase()) || c.installation_address.toLowerCase().includes(searchTerm.toLowerCase());
    const matchDept = !deptFilter || c.department_name.includes(deptFilter);
    return matchSearch && matchDept;
  });

  const handleOnboardSubmit = async (e) => {
    e.preventDefault();
    try {
      await onboardCamera(formData);
      alert(`Camera ${formData.camera_code} successfully onboarded to Model 1 GIS Asset Registry!`);
      setShowAddModal(false);
      if (onRefresh) onRefresh();
    } catch (err) {
      alert("Error onboarding camera: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-2xl flex flex-col gap-4 h-full overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Database className="text-cyan-400" size={18} />
            Model 1: Centralised CCTV Asset Registry & GIS Inventory
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Single Source of Truth for ~80,000 cameras across 26 Gujarat Government Departments
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="px-3.5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-medium text-xs rounded-xl shadow transition flex items-center gap-1.5"
        >
          <Plus size={16} /> Onboard New Camera
        </button>
      </div>

      {/* Filter Controls */}
      <div className="flex gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-2.5 text-slate-400" size={16} />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Filter by Camera Code or Address..."
            className="w-full bg-slate-950 border border-slate-800 text-slate-100 placeholder-slate-500 rounded-xl pl-9 pr-4 py-2 text-xs focus:outline-none focus:border-cyan-500 transition"
          />
        </div>
      </div>

      {/* Camera Inventory Table */}
      <div className="border border-slate-800 rounded-xl overflow-hidden">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Camera Code</th>
              <th className="p-3">Department Owner</th>
              <th className="p-3">District / Address</th>
              <th className="p-3">Vendor</th>
              <th className="p-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {filteredCams.map((c) => (
              <tr key={c.id || c.camera_code} className="hover:bg-slate-800/40 transition">
                <td className="p-3 font-mono font-bold text-cyan-400">{c.camera_code}</td>
                <td className="p-3">{c.department_name}</td>
                <td className="p-3">{c.installation_address} ({c.district})</td>
                <td className="p-3">
                  <span className="bg-slate-950 px-2 py-0.5 rounded text-[10px] border border-slate-800 font-mono">
                    {c.vendor_name}
                  </span>
                </td>
                <td className="p-3">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${c.status === 'ONLINE' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-slate-800 text-slate-400'}`}>
                    ● {c.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Onboarding Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-[9999] bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-6 shadow-2xl text-slate-100">
            <h3 className="text-base font-bold mb-4 text-cyan-400">Onboard New Camera to Model 1 Registry</h3>
            <form onSubmit={handleOnboardSubmit} className="flex flex-col gap-3 text-xs">
              <div>
                <label className="block text-slate-400 mb-1 font-semibold">Camera Code</label>
                <input
                  type="text"
                  required
                  value={formData.camera_code}
                  onChange={(e) => setFormData({...formData, camera_code: e.target.value})}
                  placeholder="e.g. CAM-GND-099"
                  className="w-full bg-slate-950 border border-slate-700 p-2 rounded-lg text-slate-100 font-mono"
                />
              </div>

              <div>
                <label className="block text-slate-400 mb-1 font-semibold">Department Owner</label>
                <input
                  type="text"
                  required
                  value={formData.department_name}
                  onChange={(e) => setFormData({...formData, department_name: e.target.value})}
                  className="w-full bg-slate-950 border border-slate-700 p-2 rounded-lg text-slate-100"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-400 mb-1 font-semibold">District</label>
                  <input
                    type="text"
                    required
                    value={formData.district}
                    onChange={(e) => setFormData({...formData, district: e.target.value})}
                    className="w-full bg-slate-950 border border-slate-700 p-2 rounded-lg text-slate-100"
                  />
                </div>
                <div>
                  <label className="block text-slate-400 mb-1 font-semibold">Vendor</label>
                  <select
                    value={formData.vendor_name}
                    onChange={(e) => setFormData({...formData, vendor_name: e.target.value})}
                    className="w-full bg-slate-950 border border-slate-700 p-2 rounded-lg text-slate-100"
                  >
                    <option value="Hikvision">Hikvision</option>
                    <option value="Dahua">Dahua</option>
                    <option value="Axis">Axis</option>
                    <option value="CP Plus">CP Plus</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-slate-400 mb-1 font-semibold">Installation Address</label>
                <input
                  type="text"
                  required
                  value={formData.installation_address}
                  onChange={(e) => setFormData({...formData, installation_address: e.target.value})}
                  placeholder="e.g. Mahatma Mandir Gate 2"
                  className="w-full bg-slate-950 border border-slate-700 p-2 rounded-lg text-slate-100"
                />
              </div>

              <div>
                <label className="block text-slate-400 mb-1 font-semibold">RTSP Stream URL</label>
                <input
                  type="text"
                  required
                  value={formData.rtsp_url}
                  onChange={(e) => setFormData({...formData, rtsp_url: e.target.value})}
                  placeholder="rtsp://admin:pass@10.240.1.1:554/stream"
                  className="w-full bg-slate-950 border border-slate-700 p-2 rounded-lg text-slate-100 font-mono"
                />
              </div>

              <div className="flex gap-2 justify-end mt-4">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-slate-300 font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg font-bold shadow"
                >
                  Register Camera
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
