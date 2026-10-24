import datetime
from db.database import SessionLocal, engine, Base
from db.models import Department, Camera, ANPRDetection, Watchlist

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 1. Seed Departments (26 Departments Mandate)
    dept_names = [
        "Home Department / Gujarat Police", "RTO / Transport Department", "Food & Civil Supplies",
        "Municipal Corporation (Ahmedabad)", "Municipal Corporation (Surat)", "Municipal Corporation (Vadodara)",
        "State Disaster Management Authority", "Forest & Environment Department", "Health & Family Welfare",
        "Education Department", "Urban Development", "Roads & Buildings Department", "Port & Transport",
        "Tourism Gujarat", "Panchayats & Rural Housing", "Revenue Department", "Agriculture & Farmers Welfare",
        "Energy & Petrochemicals", "Industries & Mines", "Labor & Employment", "Social Justice",
        "Tribal Development", "Women & Child Development", "Water Resources", "Information & Broadcasting",
        "State Crime Record Bureau (SCRB)"
    ]

    existing_depts = db.query(Department).all()
    if not existing_depts:
        depts_to_add = [Department(name=name) for name in dept_names]
        db.add_all(depts_to_add)
        db.commit()

    depts = db.query(Department).all()
    home_dept_id = depts[0].id
    rto_dept_id = depts[1].id
    food_dept_id = depts[2].id

    # 2. Seed 50 Cameras across Gujarat
    existing_cams = db.query(Camera).all()
    if not existing_cams:
        sample_cameras = []
        # Representative coordinates across Gujarat districts
        base_coords = [
            # Ahmedabad Area (CCTVs 1-15)
            ("CAM-AHM-001", "SG Highway - ISCON Cross Roads", "Ahmedabad", 23.0276, 72.5081, home_dept_id, "Hikvision"),
            ("CAM-AHM-002", "SG Highway - Pakwan Circle", "Ahmedabad", 23.0384, 72.5119, home_dept_id, "Hikvision"),
            ("CAM-AHM-003", "SG Highway - Vaishnodevi Circle", "Ahmedabad", 23.1256, 72.5372, rto_dept_id, "CP Plus"),
            ("CAM-AHM-004", "Geeta Mandir Central Bus Stand", "Ahmedabad", 23.0124, 72.5941, home_dept_id, "Dahua"),
            ("CAM-AHM-005", "Narol Circle - Highway Junction", "Ahmedabad", 22.9734, 72.6012, home_dept_id, "Hikvision"),
            ("CAM-AHM-006", "Kalupur Railway Station Plaza", "Ahmedabad", 23.0225, 72.6010, home_dept_id, "Axis"),
            ("CAM-AHM-007", "Sabarmati Riverfront East Corridor", "Ahmedabad", 23.0410, 72.5760, home_dept_id, "Hikvision"),
            ("CAM-AHM-008", "Ashram Road - Income Tax Circle", "Ahmedabad", 23.0370, 72.5690, home_dept_id, "Dahua"),
            ("CAM-AHM-009", "Paldi Cross Roads", "Ahmedabad", 23.0145, 72.5620, home_dept_id, "CP Plus"),
            ("CAM-AHM-010", "Maninagar Railway Crossing", "Ahmedabad", 22.9980, 72.6080, home_dept_id, "Hikvision"),
            ("CAM-AHM-011", "Vastrapur Lake Outer Perimeter", "Ahmedabad", 23.0350, 72.5290, home_dept_id, "Hikvision"),
            ("CAM-AHM-012", "Bapu Nagar Commercial Hub", "Ahmedabad", 23.0450, 72.6320, home_dept_id, "Dahua"),
            ("CAM-AHM-013", "Odhav Industrial Estate Checkpoint", "Ahmedabad", 23.0190, 72.6610, food_dept_id, "Hikvision"),
            ("CAM-AHM-014", "Sardar Patel Ring Road - Bopal Flyover", "Ahmedabad", 23.0290, 72.4670, rto_dept_id, "Axis"),
            ("CAM-AHM-015", "Sanand Toll Plaza", "Ahmedabad", 22.9910, 72.3810, rto_dept_id, "CP Plus"),

            # Gandhinagar Area (CCTVs 16-25)
            ("CAM-GND-016", "Infocity Gate Sector 0", "Gandhinagar", 23.1950, 72.6340, home_dept_id, "Hikvision"),
            ("CAM-GND-017", "GH-5 Circle - Mahatma Mandir", "Gandhinagar", 23.2200, 72.6480, home_dept_id, "Hikvision"),
            ("CAM-GND-018", "Chiloda Highway Junction", "Gandhinagar", 23.2450, 72.6910, rto_dept_id, "Axis"),
            ("CAM-GND-019", "Sector 21 Shopping Center", "Gandhinagar", 23.2180, 72.6390, home_dept_id, "Dahua"),
            ("CAM-GND-020", "Gujarat Police Headquarters Sector 18", "Gandhinagar", 23.2110, 72.6450, home_dept_id, "CP Plus"),
            ("CAM-GND-021", "PDPU Road Raysan Circle", "Gandhinagar", 23.1580, 72.6520, home_dept_id, "Hikvision"),
            ("CAM-GND-022", "Kudasan Cross Roads", "Gandhinagar", 23.1810, 72.6280, home_dept_id, "Hikvision"),
            ("CAM-GND-023", "GIFT City Main Entry Checkpoint", "Gandhinagar", 23.1610, 72.6840, home_dept_id, "Axis"),
            ("CAM-GND-024", "Sargasan Cross Roads", "Gandhinagar", 23.1900, 72.6090, home_dept_id, "Dahua"),
            ("CAM-GND-025", "Pethapur RTO Testing Track", "Gandhinagar", 23.2650, 72.6410, rto_dept_id, "CP Plus"),

            # Surat Area (CCTVs 26-33)
            ("CAM-SRT-026", "Ring Road Diamond Market", "Surat", 21.1950, 72.8310, home_dept_id, "Hikvision"),
            ("CAM-SRT-027", "Dumas Road Airport Circle", "Surat", 21.1410, 72.7650, home_dept_id, "Hikvision"),
            ("CAM-SRT-028", "Kamrej Toll Plaza Expressway", "Surat", 21.2780, 72.9610, rto_dept_id, "Axis"),
            ("CAM-SRT-029", "Textile Market Sahara Darwaja", "Surat", 21.1890, 72.8450, home_dept_id, "Dahua"),
            ("CAM-SRT-030", "Adajan Patia Junction", "Surat", 21.2010, 72.7980, home_dept_id, "Hikvision"),
            ("CAM-SRT-031", "Varachha Main Road", "Surat", 21.2180, 72.8620, home_dept_id, "CP Plus"),
            ("CAM-SRT-032", "Hazira Industrial Corridor", "Surat", 21.1120, 72.6410, food_dept_id, "Dahua"),
            ("CAM-SRT-033", "Sachin GIDC Checkpoint", "Surat", 21.0850, 72.8540, rto_dept_id, "Hikvision"),

            # Vadodara Area (CCTVs 34-40)
            ("CAM-VDR-034", "Alkapuri Express Tower Circle", "Vadodara", 22.3100, 73.1710, home_dept_id, "Hikvision"),
            ("CAM-VDR-035", "Golden Toll Plaza NH-48", "Vadodara", 22.3850, 73.1950, rto_dept_id, "Axis"),
            ("CAM-VDR-036", "Pandya Bridge Junction", "Vadodara", 22.3250, 73.1890, home_dept_id, "CP Plus"),
            ("CAM-VDR-037", "Makarpura GIDC Highway Entry", "Vadodara", 22.2510, 73.1980, home_dept_id, "Dahua"),
            ("CAM-VDR-038", "Sama Savli Road Checkpoint", "Vadodara", 22.3480, 73.2090, home_dept_id, "Hikvision"),
            ("CAM-VDR-039", "Waghodia Cross Roads", "Vadodara", 22.2980, 73.2380, rto_dept_id, "Hikvision"),
            ("CAM-VDR-040", "Fertilizernagar GSFC Gate", "Vadodara", 22.3680, 73.1550, food_dept_id, "Dahua"),

            # Rajkot, Dwarka, Somnath, Dahod, Valsad (CCTVs 41-50)
            ("CAM-RJK-041", "Kalawad Road KKV Hall Circle", "Rajkot", 22.2850, 70.7710, home_dept_id, "Hikvision"),
            ("CAM-RJK-042", "Gondal Road Green Land Chowk", "Rajkot", 22.2610, 70.8120, rto_dept_id, "Axis"),
            ("CAM-RJK-043", "Madhapar Chowk Highway Checkpoint", "Rajkot", 22.3210, 70.7620, home_dept_id, "CP Plus"),
            ("CAM-DWK-044", "Dwarkadhish Temple Entry Corridor", "Dwarka", 22.2390, 68.9670, home_dept_id, "Hikvision"),
            ("CAM-DWK-045", "Okha Bypass Highway Checkpoint", "Dwarka", 22.4610, 69.0710, rto_dept_id, "Axis"),
            ("CAM-SMN-046", "Somnath Temple Bypass Plaza", "Gir Somnath", 20.8880, 70.4010, home_dept_id, "Hikvision"),
            ("CAM-SMN-047", "Veraval Port Checkpoint", "Gir Somnath", 20.9080, 70.3680, rto_dept_id, "CP Plus"),
            ("CAM-DHD-048", "Dahod Inter-State Border Checkpoint", "Dahod", 22.8350, 74.2580, home_dept_id, "Hikvision"),
            ("CAM-VLS-049", "Valsad NH-48 Border Highway Gate", "Valsad", 20.6100, 72.9310, rto_dept_id, "Dahua"),
            ("CAM-VLS-050", "Vapi Industrial Belt Checkpoint", "Valsad", 20.3710, 72.9050, home_dept_id, "Hikvision")
        ]

        for code, addr, dist, lat, lng, dept_id, vendor in base_coords:
            rtsp = f"rtsp://sentinel_gateway.gujarat.gov.in:8554/live/{code}"
            webrtc = f"http://localhost:8889/live/{code}"
            c = Camera(
                camera_code=code,
                installation_address=addr,
                district=dist,
                latitude=lat,
                longitude=lng,
                department_id=dept_id,
                vendor_name=vendor,
                rtsp_url=rtsp,
                webrtc_url=webrtc,
                status="ONLINE",
                fov_azimuth=45
            )
            sample_cameras.append(c)

        db.add_all(sample_cameras)
        db.commit()

    # 3. Seed Watchlist (Including Step 4 Target Plate)
    existing_watchlist = db.query(Watchlist).all()
    if not existing_watchlist:
        watchlist_items = [
            Watchlist(plate_number="GJ01HK9988", reason="Step 4 Evaluation Target / Stolen SUV - FIR #402/2026", category="Stolen Vehicle", severity="CRITICAL"),
            Watchlist(plate_number="GJ18AB1234", reason="Wanted Suspect Vehicle - Crime Branch Alert", category="Wanted Criminal", severity="CRITICAL"),
            Watchlist(plate_number="GJ05CD5678", reason="Unpaid Transport Fines & Blacklisted RTO", category="Blacklisted", severity="HIGH"),
            Watchlist(plate_number="GJ06EF9012", reason="Missing Person Probe Vehicle", category="Missing Person", severity="MEDIUM")
        ]
        db.add_all(watchlist_items)
        db.commit()

    # 4. Seed Step 4 Demo Route Trajectory for GJ01HK9988
    cams = db.query(Camera).all()
    cam_dict = {c.camera_code: c.id for c in cams}
    
    existing_detections = db.query(ANPRDetection).all()
    if not existing_detections and "CAM-AHM-004" in cam_dict:
        now = datetime.datetime.utcnow()
        # Chronological trajectory for Step 4 Target Vehicle GJ01HK9988
        demo_trajectory = [
            ("CAM-AHM-004", "GJ01HK9988", True, "Stolen Vehicle", now - datetime.timedelta(minutes=45)), # Geeta Mandir
            ("CAM-AHM-005", "GJ01HK9988", True, "Stolen Vehicle", now - datetime.timedelta(minutes=30)), # Narol Circle
            ("CAM-AHM-015", "GJ01HK9988", True, "Stolen Vehicle", now - datetime.timedelta(minutes=15)), # Sanand Toll
            ("CAM-GND-016", "GJ01HK9988", True, "Stolen Vehicle", now - datetime.timedelta(minutes=5))   # Infocity GND
        ]

        detections = []
        for code, plate, is_hit, cat, dt in demo_trajectory:
            if code in cam_dict:
                d = ANPRDetection(
                    camera_id=cam_dict[code],
                    detected_plate=plate,
                    confidence=0.96,
                    vehicle_type="SUV",
                    vehicle_color="Black",
                    is_watchlist_hit=is_hit,
                    watchlist_category=cat,
                    detected_at=dt,
                    snapshot_url=f"/snapshots/demo_{code}.jpg"
                )
                detections.append(d)

        # Add routine detections for other cameras
        routine_plates = ["GJ01AB1111", "GJ18XY2222", "GJ05ZZ3333", "GJ27AA4444"]
        for idx, (code, cid) in enumerate(cam_dict.items()):
            if idx > 4:
                d = ANPRDetection(
                    camera_id=cid,
                    detected_plate=routine_plates[idx % len(routine_plates)],
                    confidence=0.94,
                    vehicle_type="Car",
                    vehicle_color="White",
                    is_watchlist_hit=False,
                    detected_at=now - datetime.timedelta(minutes=idx * 2)
                )
                detections.append(d)

        db.add_all(detections)
        db.commit()

    db.close()
