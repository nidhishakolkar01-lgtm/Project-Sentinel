import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '/api/v1';
const API_KEY = import.meta.env.VITE_API_KEY || 'sentinel_sec_key_2026_auth';

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY
  }
});

export const fetchCameras = async (filters = {}) => {
  try {
    const res = await apiClient.get('/cameras', { params: filters });
    return res.data;
  } catch (err) {
    console.warn("API Offline or unreachable, loading regional GIS camera inventory", err.message);
    return getMockCameras();
  }
};

export const fetchVehicleRoute = async (plate) => {
  try {
    const res = await apiClient.get('/tracking/route', { params: { plate } });
    return res.data;
  } catch (err) {
    console.warn("API Offline, returning mock trajectory", err.message);
    return getMockTrajectory(plate);
  }
};

export const fetchDetections = async (filters = {}) => {
  try {
    const res = await apiClient.get('/analytics/detections', { params: filters });
    return res.data;
  } catch (err) {
    return getMockDetections();
  }
};

export const onboardCamera = async (cameraData) => {
  const res = await apiClient.post('/cameras/onboard', cameraData);
  return res.data;
};

// Fallback Mock Datasets if Backend is offline
function getMockCameras() {
  return [
    { id: 1, camera_code: "CAM-AHM-001", department_name: "Law Enforcement & Public Safety", vendor_name: "Hikvision", latitude: 23.0276, longitude: 72.5081, district: "Ahmedabad", installation_address: "SG Highway - ISCON Cross Roads", status: "ONLINE", fov_azimuth: 45 },
    { id: 2, camera_code: "CAM-AHM-004", department_name: "Law Enforcement & Public Safety", vendor_name: "Dahua", latitude: 23.0124, longitude: 72.5941, district: "Ahmedabad", installation_address: "Geeta Mandir Central Bus Stand", status: "ONLINE", fov_azimuth: 90 },
    { id: 3, camera_code: "CAM-AHM-005", department_name: "Law Enforcement & Public Safety", vendor_name: "Hikvision", latitude: 22.9734, longitude: 72.6012, district: "Ahmedabad", installation_address: "Narol Circle Highway Junction", status: "ONLINE", fov_azimuth: 180 },
    { id: 4, camera_code: "CAM-AHM-015", department_name: "RTO / Transport Department", vendor_name: "CP Plus", latitude: 22.9910, longitude: 72.3810, district: "Ahmedabad", installation_address: "Sanand Toll Plaza", status: "ONLINE", fov_azimuth: 270 },
    { id: 5, camera_code: "CAM-GND-016", department_name: "Law Enforcement & Public Safety", vendor_name: "Hikvision", latitude: 23.1950, longitude: 72.6340, district: "Gandhinagar", installation_address: "Infocity Gate Sector 0", status: "ONLINE", fov_azimuth: 0 },
    { id: 6, camera_code: "CAM-GND-017", department_name: "Law Enforcement & Public Safety", vendor_name: "Hikvision", latitude: 23.2200, longitude: 72.6480, district: "Gandhinagar", installation_address: "GH-5 Circle Mahatma Mandir", status: "ONLINE", fov_azimuth: 45 },
    { id: 7, camera_code: "CAM-SRT-026", department_name: "Law Enforcement & Public Safety", vendor_name: "Axis", latitude: 21.1950, longitude: 72.8310, district: "Surat", installation_address: "Ring Road Diamond Market", status: "ONLINE", fov_azimuth: 120 },
    { id: 8, camera_code: "CAM-VDR-034", department_name: "Law Enforcement & Public Safety", vendor_name: "Hikvision", latitude: 22.3100, longitude: 73.1710, district: "Vadodara", installation_address: "Alkapuri Express Tower", status: "ONLINE", fov_azimuth: 210 }
  ];
}

function getMockTrajectory(plate) {
  const p = plate ? plate.toUpperCase().replace("-", "").replace(" ", "") : "GJ01HK9988";
  return {
    target_plate: p,
    total_checkpoints: 4,
    total_distance_km: 42.5,
    first_seen: new Date(Date.now() - 3600000).toISOString(),
    last_seen: new Date().toISOString(),
    trajectory: [
      { sequence: 1, camera_id: 2, camera_code: "CAM-AHM-004", location_name: "Geeta Mandir Central Bus Stand, Ahmedabad", district: "Ahmedabad", latitude: 23.0124, longitude: 72.5941, detected_plate: p, timestamp: new Date(Date.now() - 3600000).toISOString(), confidence: 0.98 },
      { sequence: 2, camera_id: 3, camera_code: "CAM-AHM-005", location_name: "Narol Circle Highway Junction, Ahmedabad", district: "Ahmedabad", latitude: 22.9734, longitude: 72.6012, detected_plate: p, timestamp: new Date(Date.now() - 2400000).toISOString(), confidence: 0.96 },
      { sequence: 3, camera_id: 4, camera_code: "CAM-AHM-015", location_name: "Sanand Toll Plaza, Ahmedabad", district: "Ahmedabad", latitude: 22.9910, longitude: 72.3810, detected_plate: p, timestamp: new Date(Date.now() - 1200000).toISOString(), confidence: 0.97 },
      { sequence: 4, camera_id: 5, camera_code: "CAM-GND-016", location_name: "Infocity Gate Sector 0, Gandhinagar", district: "Gandhinagar", latitude: 23.1950, longitude: 72.6340, detected_plate: p, timestamp: new Date().toISOString(), confidence: 0.99 }
    ]
  };
}

function getMockDetections() {
  return [
    { id: 101, camera_code: "CAM-GND-016", location_name: "Infocity Gate Sector 0", district: "Gandhinagar", detected_plate: "GJ01HK9988", confidence: 0.99, vehicle_type: "SUV", vehicle_color: "Black", is_watchlist_hit: true, watchlist_category: "Stolen Vehicle", detected_at: new Date().toISOString() },
    { id: 102, camera_code: "CAM-AHM-015", location_name: "Sanand Toll Plaza", district: "Ahmedabad", detected_plate: "GJ01HK9988", confidence: 0.97, vehicle_type: "SUV", vehicle_color: "Black", is_watchlist_hit: true, watchlist_category: "Stolen Vehicle", detected_at: new Date(Date.now() - 1200000).toISOString() },
    { id: 103, camera_code: "CAM-AHM-001", location_name: "ISCON Cross Roads", district: "Ahmedabad", detected_plate: "GJ18AB1234", confidence: 0.94, vehicle_type: "Sedan", vehicle_color: "White", is_watchlist_hit: false, watchlist_category: null, detected_at: new Date(Date.now() - 1800000).toISOString() }
  ];
}
