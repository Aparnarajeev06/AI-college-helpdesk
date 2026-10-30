# ============================================================
# NCERC Campus Data — Audit version
#
# Each entry carries a "confidence" field:
#   "verified"           - claim explicitly stated on the official page cited by source_url
#   "verified-partial"   - main fact verified; one or more fine-grained details (e.g. exact floor
#                          number, exact room count) are sourced from floor-plan data or a secondary
#                          NCERC page rather than the primary infrastructure/facilities page
#   "unverified"         - present in prior dataset but NOT confirmed by any official page inspected;
#                          the AI must say it cannot confirm the exact detail
#
# Audit date : 2026-10-22
# Sources checked :
#   https://ncerc.ac.in/infrastructure  (cached page + Google-indexed text)
#   https://ncerc.ac.in/facilities      (live page + Google-indexed text)
#   https://ncerc.ac.in/sports          (Google-indexed text via ncerc.ac.in/sports)
# ============================================================

ncerc_data = {

    # ── LIBRARY ──────────────────────────────────────────────
    # OFFICIALLY VERIFIED: "Central Library situated on the ground floor of the Brahmagupta block"
    # Source: ncerc.ac.in/infrastructure (Google-cached text)
    "library": {
        "name": "NCERC Central Library",
        "aliases": ["central library", "library", "digital library", "reading room"],
        "block": "Brahmagupta Block",
        "floor": "Ground Floor",
        "location": "Ground floor of the Brahmagupta Block",
        "description": (
            "The Central Library is situated on the ground floor of the Brahmagupta Block. "
            "It provides books, journals, periodicals, digital resources, and ILMS-based "
            "cataloguing services for students and staff."
        ),
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified",
        "tour_url": "https://ncerc.ac.in/360/",
    },

    # ── CANTEEN ──────────────────────────────────────────────
    # OFFICIALLY VERIFIED: campus canteen confirmed on infrastructure/facilities pages.
    # TIMING ("8 AM – 5 PM including Saturday"): not found in the live page text inspected;
    # treat as unverified-partial until the college confirms it on an official page.
    "canteen": {
        "name": "NCERC Canteen",
        "aliases": ["canteen", "cafeteria", "food court", "king nala canteen"],
        "location": "NCERC Campus",
        "description": (
            "The campus canteen serves quality food and refreshments to students and staff. "
            "Exact opening hours have not been confirmed from the official website; "
            "please check the college notice board or contact the college office for current timings."
        ),
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified-partial",
        "tour_url": "https://ncerc.ac.in/360/",
    },

    # ── FITNESS CENTRE / GYM ─────────────────────────────────
    # OFFICIALLY VERIFIED: gym is inside Bhaskara Block.
    # "Basement Floor" comes from floor-plan data, confirmed by ncerc.ac.in/infrastructure page text.
    "fitness_centre": {
        "name": "Fitness Centre",
        "aliases": ["gym", "gymnasium", "health club", "fitness center", "fitness zone"],
        "block": "Bhaskara Block",
        "floor": "Basement Floor",
        "location": "Bhaskara Block, Basement Floor",
        "description": (
            "The ultra-modern gymnasium (approx. 100 sq m) is located in the basement of "
            "Bhaskara Block. It provides modern weight-training and cardio equipment for "
            "students and staff, supervised by physical education staff."
        ),
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified",
        "tour_url": "https://ncerc.ac.in/360/",
    },

    # ── TRANSPORTATION ────────────────────────────────────────
    # OFFICIALLY VERIFIED: bus service mentioned on infrastructure page.
    "transportation": {
        "name": "College Transportation",
        "aliases": ["transport", "transportation", "college bus", "college buses", "bus routes"],
        "location": "NCERC Campus",
        "description": (
            "NCERC provides college bus transportation for students and staff. "
            "For current bus routes and schedules, contact the college transport office."
        ),
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified",
        "tour_url": "https://ncerc.ac.in/360/",
    },

    # ── AUDITORIUM ────────────────────────────────────────────
    # OFFICIALLY VERIFIED: Auditorium is in Brahmagupta Block, capacity ~800.
    # "Second Floor" comes from the project's floor-plan data; the official infrastructure
    # page text confirms the block but does not explicitly state "second floor" in the
    # indexed text. Marked verified-partial accordingly.
    "auditorium": {
        "name": "NCERC Main Auditorium",
        "aliases": ["auditorium", "audi", "college auditorium", "main auditorium", "brahmagupta auditorium"],
        "block": "Brahmagupta Block",
        "floor": "Second Floor",
        "location": "Brahmagupta Block (exact floor not confirmed by official page text)",
        "description": (
            "The Main Auditorium is located in Brahmagupta Block with a seating capacity "
            "of approximately 800 people. It is used for cultural programs, academic seminars, "
            "guest lectures, and college ceremonies. The exact floor number has not been "
            "independently confirmed from the official website text."
        ),
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified-partial",
        "tour_url": "https://ncerc.ac.in/360/",
    },

    # ── PLAYGROUND & OUTDOOR SPORTS ──────────────────────────
    # OFFICIALLY VERIFIED: playground ~16,800 sq m on campus grounds; courts confirmed:
    # basketball, volleyball, football, cricket, badminton, kabaddi, handball, hockey.
    # Source: ncerc.ac.in/sports (indexed text confirming sports ground area and courts)
    "sports_playground": {
        "name": "Playground & Outdoor Sports Facilities",
        "aliases": [
            "playground", "play ground", "sports ground", "ground", "athletic field",
            "football ground", "cricket ground", "outdoor sports", "sports",
            "badminton court", "kabaddi", "handball", "hockey ground",
        ],
        "block": "Campus Grounds",
        "floor": None,
        "location": "NCERC Campus Grounds",
        "description": (
            "The NCERC sports ground spans approximately 16,800 square metres on the college campus. "
            "Confirmed courts and fields include: Basketball, Volleyball, Football, Cricket, "
            "Badminton, Kabaddi, Handball, and Hockey. Physical education coaches support student "
            "training and regular inter-collegiate tournaments."
        ),
        "source_url": "https://ncerc.ac.in/sports",
        "confidence": "verified",
        "tour_url": "https://ncerc.ac.in/360/",
    },

    # ── BASKETBALL COURT ─────────────────────────────────────
    # OFFICIALLY VERIFIED via ncerc.ac.in/sports page.
    "basketball_court": {
        "name": "Basketball Court",
        "aliases": ["basketball court", "basketball", "basket ball", "basket ball court"],
        "block": "Campus Grounds",
        "floor": None,
        "location": "NCERC Campus Grounds",
        "description": (
            "The basketball court is an outdoor court on the NCERC campus sports grounds, "
            "confirmed as one of the official sports facilities available to students."
        ),
        "source_url": "https://ncerc.ac.in/sports",
        "confidence": "verified",
        "tour_url": "https://ncerc.ac.in/360/",
    },

    # ── KAPILA BLOCK ─────────────────────────────────────────
    # OFFICIALLY VERIFIED: 60,000 sq ft; MBA, MCA, PG Library, computer labs,
    # lecture halls, tutorial rooms, faculty cabins, seminar halls, boardroom, yoga hall.
    # Source: ncerc.ac.in/infrastructure (Google-indexed official text)
    "kapila_block": {
        "name": "Kapila Block",
        "aliases": [
            "kapila", "kapila block", "kapila building", "management block",
            "mba block", "mca block",
        ],
        "block": "Kapila Block",
        "floor": None,
        "location": "Kapila Block",
        "description": (
            "Kapila Block, named after sage Kapila, has a built-up area of 60,000 sq. ft. "
            "It houses the MBA and MCA Departments, a PG Library, computer laboratories, "
            "lecture halls, tutorial rooms, faculty cabins, seminar halls, a boardroom, "
            "and a yoga hall."
        ),
        "facilities": [
            "MBA Department",
            "MCA Department",
            "PG Library",
            "Board Room",
            "Tutorial Rooms",
            "Faculty Cabins",
            "Seminar Halls",
            "Yoga Hall",
            "Computer Laboratories",
        ],
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified",
        "tour_url": "https://ncerc.ac.in/360/",
    },

    # ── BRAHMAGUPTA BLOCK ────────────────────────────────────
    # OFFICIALLY VERIFIED: 30,000 sq ft; Central Library (ground floor); Auditorium (~800 seats).
    # Automobile Workshop and Electronics Laboratory mentioned in prior dataset —
    # not found in the official indexed page text; marked verified-partial.
    "brahmagupta_block": {
        "name": "Brahmagupta Block",
        "aliases": [
            "brahmagupta", "brahmagupta block", "brahmagupta building", "brahmaguptha block",
        ],
        "block": "Brahmagupta Block",
        "floor": None,
        "location": "Brahmagupta Block",
        "description": (
            "Brahmagupta Block, named after the ancient astronomer Brahmagupta, has a total "
            "area of 30,000 sq. ft. It houses the NCERC Central Library on the ground floor "
            "and the Main Auditorium (seating ~800 people). "
            "An automobile workshop and electronics laboratory are also reported in this block "
            "but their presence has not been independently confirmed from the official page text."
        ),
        "facilities": [
            "Central Library (Ground Floor) — verified",
            "Main Auditorium (~800 seats) — verified",
            "Automobile Workshop — not independently confirmed from official page text",
            "Electronics Laboratory — not independently confirmed from official page text",
        ],
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified-partial",
        "tour_url": "https://ncerc.ac.in/360/",
    },

    # ── VARAHAMIHIRA BLOCK ───────────────────────────────────
    # OFFICIALLY VERIFIED: 30,000 sq ft; main workshop building for Mechanical Engineering;
    # CORRECTION: official source says 4 Electrical Engineering labs (previous dataset said 3).
    # Civil Engineering lab: not found in the official indexed text; marked verified-partial.
    "varahamihira_block": {
        "name": "Varahamihira Block",
        "aliases": [
            "varahamihira", "varahamihira block", "varahmihira", "varahamihira building",
            "workshop block", "main workshop building",
        ],
        "block": "Varahamihira Block",
        "floor": None,
        "location": "Varahamihira Block",
        "description": (
            "Varahamihira Block, named after the astronomer Varahamihira, is the main workshop "
            "building with an area of 30,000 sq. ft. It houses the workshops of the Mechanical "
            "Engineering Department and four laboratories of the Electrical Engineering Department. "
            "A Civil Engineering lab is reported but not independently confirmed from the official page text."
        ),
        "facilities": [
            "Mechanical Engineering Workshops — verified",
            "4 Electrical Engineering Laboratories — verified",
            "Civil Engineering Lab — not independently confirmed from official page text",
        ],
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified-partial",
        "tour_url": "https://ncerc.ac.in/360/",
    },

    # ── BHASKARA BLOCK ───────────────────────────────────────
    # OFFICIALLY VERIFIED: Bhaskara Block is in Bhaskara Block; gym in basement confirmed.
    # 1 lakh sq ft, first-year classrooms, KTU Exam Cell, NSS/NCC confirmed via official text.
    # Billiards room mentioned in prior dataset — not found in official indexed text.
    "bhaskara_block": {
        "name": "Bhaskara Block",
        "aliases": [
            "bhaskara", "bhaskara block", "bhaskara building", "bhaskaracharya block",
        ],
        "block": "Bhaskara Block",
        "floor": None,
        "location": "Bhaskara Block",
        "description": (
            "Bhaskara Block, named after mathematician Bhaskaracharya, is the first academic block "
            "with a built-up area of approximately 1 lakh sq. ft. It houses first-year classrooms, "
            "electronics and computer science laboratories, language lab, drawing halls, KTU Exam Cell, "
            "KTU Seminar Hall, Medical Room, Innovation Hub, NCC Office, NSS Office, "
            "Department of Physical Education, faculty cabins, tutorial rooms, a board room, "
            "conference room, and store rooms. "
            "The basement houses the ultra-modern gymnasium. "
            "A billiards room is reported in this block but not confirmed from the official page text."
        ),
        "facilities": [
            "Board Room",
            "Conference Room",
            "Faculty Cabins",
            "Tutorial Rooms",
            "First Year Classrooms",
            "Electronics Laboratories",
            "Computer Science Laboratories",
            "Language Lab",
            "Drawing Halls",
            "KTU Exam Cell",
            "KTU Seminar Hall",
            "Medical Room",
            "Innovation Hub",
            "NCC Office",
            "NSS Office",
            "Department of Physical Education",
            "Gymnasium (Basement Floor) — verified",
            "Billiards Room (Basement Floor) — not independently confirmed from official page text",
        ],
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified-partial",
        "tour_url": "https://ncerc.ac.in/360/",
    },

    # ── ARYABHATTA BLOCK ─────────────────────────────────────
    # OFFICIALLY VERIFIED: hexagonal, six-storied, 1.25 lakh sq ft; Principal's Office,
    # Academic Office, Placement Office, CSE/ECE/EEE/ME/MTR departments, smart classrooms,
    # faculty cabins, seminar halls, Advanced Computing Lab, lifts.
    "aryabhatta_block": {
        "name": "Aryabhatta Block",
        "aliases": [
            "aryabhatta", "aryabhatta block", "aryabhatta building", "main academic block",
        ],
        "block": "Aryabhatta Block",
        "floor": None,
        "location": "Aryabhatta Block",
        "description": (
            "Aryabhatta Block, named after the astronomer Aryabhatta, is a hexagonal six-storied "
            "building with a built-up area of 1.25 lakh sq. ft. It houses 5 UG/PG departments "
            "(CSE, ECE, EEE, ME, MTR), the Principal's Office, Academic Office, Placement Office, "
            "conference room, board room, faculty cabins, seminar halls, Advanced Computing Lab, "
            "smart classrooms, tutorial rooms, and lifts."
        ),
        "facilities": [
            "Principal's Office (First Floor)",
            "Academic Office (First Floor)",
            "Placement Office",
            "Advanced Computing Lab (First Floor)",
            "5 UG and PG Departments (CSE, ECE, EEE, ME, MTR)",
            "Smart Classrooms",
            "Faculty Cabins",
            "Seminar Halls",
            "Board Room",
            "Lifts",
        ],
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified",
        "tour_url": "https://ncerc.ac.in/360/",
    },

    # ── ADMINISTRATIVE & ACADEMIC OFFICES ────────────────────
    # OFFICIALLY VERIFIED: Principal's Office and Academic Office are in Aryabhatta Block.
    # "First Floor" comes from floor-plan data; confirmed indirectly by NCERC official text.
    "administrative_office": {
        "name": "Administrative & Academic Offices",
        "aliases": [
            "administrative office", "admin office", "administration office",
            "college office", "academic office", "principal office", "principals office",
        ],
        "block": "Aryabhatta Block",
        "floor": "First Floor",
        "location": "Aryabhatta Block, First Floor",
        "description": (
            "The Academic Office and Principal's Office are located in Aryabhatta Block. "
            "General college administration, admissions enquiries, and office matters are handled here. "
            "KTU and Autonomous examination enquiries are handled at the KTU Exam Cell in Bhaskara Block. "
            "Contact: office@ncerc.ac.in | +91 9656000005."
        ),
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified-partial",
        "tour_url": "https://ncerc.ac.in/360/",
    },

    # ── HOSTELS ──────────────────────────────────────────────
    # OFFICIALLY VERIFIED: Kasturba (Block C, ~500 women), Kamala (Block A, ~300 women),
    # Priyadarshini / Indira Gandhi (Block B, ~100 persons), men's hostel.
    # CORRECTION: previous dataset said "Kasturba Ladies' Hostel 500 girls" and
    # "Men's Hostel 500 boys" as a single block — actually multiple blocks.
    # Sivasree Apartments: not found in the official indexed text; marked unverified.
    "hostels": {
        "name": "NCERC Hostels",
        "aliases": [
            "hostel", "hostels", "ladies hostel", "mens hostel", "boys hostel",
            "girls hostel", "kasturba", "priyadarshini", "kamala",
        ],
        "block": "Campus Hostels",
        "floor": None,
        "location": "NCERC Campus",
        "description": (
            "NCERC provides separate hostel accommodation for boys and girls. "
            "Women's hostels: Kasturba (Block C, ~500 students), Kamala/Kamala Nehru (Block A, ~300 students, "
            "with optional AC rooms), and Priyadarshini/Indira Gandhi (Block B, ~100 persons — PG students "
            "and faculty). Men's hostel accommodates students in deluxe/semi-deluxe rooms. "
            "All hostels offer Wi-Fi, hygienic mess, and fitness/recreation facilities. "
            "Note: 'Sivasree Apartments' listed in prior data has not been confirmed from the official page."
        ),
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified-partial",
        "tour_url": "https://ncerc.ac.in/360/",
    },

    # ── FLOOR-BY-FLOOR ROOM DIRECTORIES ──────────────────────
    # Confidence: "verified-partial" — room numbers sourced from floor-plan data shared
    # with the project. The block-floor assignments are confirmed; individual room numbers
    # should be verified against physical signage or the college office.

    "bhaskara_ground_floor": {
        "name": "Bhaskara Block - Ground Floor",
        "block": "Bhaskara Block",
        "floor": "Ground Floor",
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified-partial",
        "tour_url": "https://ncerc.ac.in/360/",
        "rooms": {
            "110": "NSS Office",
            "101": "Faculty Cabins",
            "111": "Classroom 111",
            "112": "Classroom 112",
            "105": "Electronics Circuits Lab",
            "106": "Digital Electronics Lab",
        },
        "facilities": [
            "Medical Room",
            "KTU Exam Cell",
            "KTU Seminar Hall",
            "Innovation Hub",
            "Chief Innovation Officer's Room",
            "Store Room",
            "Department of Physical Education",
            "Advanced Instrumentation Lab",
            "NCC Office",
            "Engineering Chemistry Lab",
            "UPS Room",
            "Lift",
            "Entrance",
            "Staff Toilets",
            "Students' Toilets",
            "Emergency Exit",
            "Fire Exit",
        ],
    },

    "bhaskara_basement": {
        "name": "Bhaskara Block - Basement Floor",
        "block": "Bhaskara Block",
        "floor": "Basement Floor",
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified-partial",
        "tour_url": "https://ncerc.ac.in/360/",
        "facilities": [
            "Gymnasium — verified",
            "Department of Physical Education",
            "Students' Toilets",
            "Store Room",
            "P.E. Store",
        ],
    },

    "aryabhatta_ground_floor": {
        "name": "Aryabhatta Block - Ground Floor",
        "block": "Aryabhatta Block",
        "floor": "Ground Floor",
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified-partial",
        "tour_url": "https://ncerc.ac.in/360/",
        "rooms": {
            "101": "Classroom",
            "102": "Boys' Common Room",
            "103": "AA NCERC",
            "105": "Internet Technologies Lab",
            "106": "Advanced Simulation Lab",
            "110": "CASET Lab",
            "111": "Advanced Software Lab",
            "113": "M.Tech Classroom",
            "114": "Girls' Common Room",
            "115": "Tutorial Room",
        },
        "facilities": [
            "Lift",
            "Entrance",
            "Students' Toilet - Gents",
            "Students' Toilet - Ladies",
            "Staff Toilet - Gents",
            "Staff Toilet - Ladies",
            "Emergency Exit",
            "Fire Exit",
        ],
    },

    "aryabhatta_first_floor": {
        "name": "Aryabhatta Block - First Floor",
        "block": "Aryabhatta Block",
        "floor": "First Floor",
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified-partial",
        "tour_url": "https://ncerc.ac.in/360/",
        "rooms": {
            "201": "Smart Classroom - ME",
            "202": "Classroom - ME",
            "203": "Tutorial Room",
            "216": "Classroom - ME",
            "218": "Classroom - CSE",
            "226": "Advanced Computing Lab",
            "228": "Classroom - CSE",
            "229": (
                "Smart Classroom - CSE / Advanced CADCAM Lab "
                "(the supplied details list both for room 229; "
                "confirm the assignment)"
            ),
        },
        "room_ranges": {
            "205-214": "ME Faculty Cabins",
            "221-225": "CSE Faculty Cabins",
        },
        "facilities": [
            "Academic Office",
            "Principal's Office",
            "Lift",
            "Students' Toilet - Gents",
            "Students' Toilet - Ladies",
            "Staff Toilet - Gents",
            "Staff Toilet - Ladies",
            "Emergency Exit",
            "Fire Exit",
        ],
    },

    "aryabhatta_second_floor": {
        "name": "Aryabhatta Block - Second Floor",
        "block": "Aryabhatta Block",
        "floor": "Second Floor",
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified-partial",
        "tour_url": "https://ncerc.ac.in/360/",
        "rooms": {
            "301": "Smart Classroom - EEE",
            "302": "Classroom - EEE",
            "303": "Classroom - M.Tech",
            "316": "Classroom - EEE",
            "317": "IQAC Conference Room",
            "317A": "Classroom - M.Tech",
            "318": "Classroom - CSE",
            "331": "Smart Classroom - CSE",
            "332": "Classroom - CSE",
            "333": "Classroom - CSE",
        },
        "room_ranges": {
            "305-314": "EEE Faculty Cabins",
            "320-329": "CSE Faculty Cabins",
        },
        "facilities": [
            "IQAC Office",
            "Director's Office",
            "Lift",
            "Emergency Exit",
            "Fire Exit",
            "Staff Toilets - Gents and Ladies",
            "Students' Toilet - Ladies",
        ],
    },

    "aryabhatta_third_floor": {
        "name": "Aryabhatta Block - Third Floor",
        "block": "Aryabhatta Block",
        "floor": "Third Floor",
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified-partial",
        "tour_url": "https://ncerc.ac.in/360/",
        "rooms": {
            "401": "Classroom - MTR",
            "402": "Classroom - MTR",
            "403": "Tutorial Room",
            "416": "Smart Classroom - MTR",
            "418": "Classroom - ECE",
            "433": "Classroom - M.Tech",
            "434": "Classroom - ECE",
            "435": "Smart Classroom - ECE",
        },
        "room_ranges": {
            "405-414": "MTR Faculty Cabins",
            "420-429": "ECE Faculty Cabins",
        },
        "facilities": [
            "Board Room - separate room, number not confirmed",
            "NCPIR Office",
            "Lift",
            "Emergency Exit",
            "Fire Exit",
            "Staff Toilets - Gents and Ladies",
            "Students' Toilet - Ladies",
        ],
    },

    "aryabhatta_fourth_floor": {
        "name": "Aryabhatta Block - Fourth Floor",
        "block": "Aryabhatta Block",
        "floor": "Fourth Floor",
        "source_url": "https://ncerc.ac.in/infrastructure",
        "confidence": "verified-partial",
        "tour_url": "https://ncerc.ac.in/360/",
        "rooms": {
            "501": "Seminar Hall - CSE",
            "504": "Classroom",
            "505": "Classroom - M.Tech",
            "505A": "Classroom - M.Tech",
            "506": "Classroom",
            "509": "Classroom - M.Tech",
            "510": "Seminar Hall - ME",
        },
        "facilities": [
            "Dining Room",
            "Research Lab",
            "VLSI and Embedded System Lab",
            "Cyber Security Lab - CSE",
            "Research Lab - CSE",
            "Sick Room - Gents",
            "Sick Room - Ladies",
            "Staff Toilet - Gents",
            "Students' Toilet - Ladies",
            "Lift",
            "Emergency Exit",
            "Fire Exit",
        ],
    },
}
