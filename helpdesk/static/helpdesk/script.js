document.addEventListener("DOMContentLoaded", () => {
    const questionInput = document.getElementById("question");
    const chatForm = document.getElementById("chat-form");
    const askButton = document.getElementById("ask-button");
    const chatMessages = document.getElementById("chat-messages");
    const typingIndicator = document.getElementById("typing-indicator");
    const dataElement = document.getElementById("ncerc-data");

    const tourUrl = "https://ncerc.ac.in/360/";
    const campusMapUrl =
        "https://www.google.com/maps/search/?api=1&query=" +
        encodeURIComponent("Nehru College of Engineering and Research Centre");

    let ncercData = {};

    if (dataElement) {
        try {
            ncercData = JSON.parse(dataElement.textContent || "{}");
        } catch (error) {
            console.error("Could not read NCERC campus data:", error);
        }
    }

    // ==============================
    // TEXT NORMALIZATION
    // ==============================

    const normalize = (value) =>
        String(value || "")
            .toLowerCase()
            .replace(/&/g, " and ")
            .replace(/[’']/g, "")
            .replace(/[^a-z0-9\s-]/g, " ")
            .replace(/\s+/g, " ")
            .trim();

    function expandQuestion(question) {
        return normalize(question)
            .replace(/\bwhere is\b/g, " location ")
            .replace(/\bwhere can i find\b/g, " location ")
            .replace(/\b(?:how can i reach|how do i get to|how to reach|directions to|can you direct me to)\b/g, " location ")
            .replace(/\b(?:what is the location of|where can i locate)\b/g, " location ")
            .replace(/\b(?:location of|located at|located in)\b/g, " location ")
            .replace(/\bcentral library\b/g, " library ")
            .replace(/\bfitness center\b/g, " fitness centre ")
            .replace(/\bgym\b/g, " fitness centre ")
            .replace(/\bcafeteria\b/g, " canteen ")
            .replace(/\bexamination cell\b/g, " exam cell ")
            .replace(/\b(?:bus|buses|transport|transportation services?)\b/g, " transportation ")
            .replace(/\broom numbers?\b/g, " room ")
            .replace(/\bclassroom\b/g, " room ")
            .replace(/\bdepartment of\b/g, " ")
            .replace(/\bdept\b/g, " department ")
            .replace(/\btimings\b/g, " timing ")
            .replace(/\b(?:when does|when is)\b/g, " timing ")
            .replace(/\bworking hours\b/g, " timing ")
            .replace(/\bopening hours\b/g, " timing ")
            .replace(/\bopen at\b/g, " timing ")
            .replace(/\bclose at\b/g, " timing ")
            .replace(/\bai and ml\b/g, " artificial intelligence machine learning ")
            .replace(
                /\bartificial intelligence and machine learning\b/g,
                " artificial intelligence machine learning "
            );
    }

    // ==============================
    // SAFE MESSAGE RENDERING
    // ==============================

    function addMessage(text, sender = "bot", options = {}) {
        if (!chatMessages) return;

        const message = document.createElement("div");
        message.className = `message ${sender}-message`;

        const content = document.createElement("div");
        content.className = "message-content";
        content.textContent = text || "";

        if (sender === "bot" && options.mode) {
            const label = document.createElement("span");
            label.className = "message-label";
            if (options.mode === "ai") {
                if (options.provider === "openai") {
                    label.textContent = "AI-generated answer · OpenAI";
                } else if (options.provider === "ollama") {
                    label.textContent = "AI-generated answer · local model";
                } else if (options.provider) {
                    label.textContent = `AI-generated answer · ${options.provider}`;
                } else {
                    label.textContent = "AI-generated answer · local model";
                }
            } else if (options.mode === "fallback") {
                label.textContent = "Local rule-based fallback";
            } else {
                label.textContent = "Clarification";
            }
            message.appendChild(label);
        }

        message.appendChild(content);

        // Highlight block, floor and room details.
        if (sender === "bot" && options.location) {
            const details = document.createElement("div");
            details.className = "location-details";

            const fields = [
                ["FACILITY", options.location.facility],
                ["BLOCK", options.location.block],
                ["FLOOR", options.location.floor],
                ["ROOM NUMBER", options.location.room],
                ["LOCATION", options.location.location],
                ["TIMINGS", options.location.timing]
            ];

            fields.forEach(([label, value]) => {
                if (!value) return;

                const card = document.createElement("div");
                card.className = "location-card";

                const heading = document.createElement("span");
                heading.className = "location-label";
                heading.textContent = label;

                const valueElement = document.createElement("span");
                valueElement.className = "location-value";
                valueElement.textContent = value;

                card.append(heading, valueElement);
                details.appendChild(card);
            });

            if (details.children.length > 0) {
                message.appendChild(details);
            }
        }

        if (
            sender === "bot" &&
            Array.isArray(options.links) &&
            options.links.length
        ) {
            const actions = document.createElement("div");
            actions.className = options.location
                ? "message-actions location-actions"
                : "message-actions";

            options.links.forEach(({ href, label }) => {
                const link = document.createElement("a");
                link.href = href;
                link.textContent = label;
                link.target = "_blank";
                link.rel = "noopener noreferrer";
                link.className = "message-link";
                actions.appendChild(link);
            });

            message.appendChild(actions);
        }

        if (options.image) {
            const image = document.createElement("img");
            image.src = options.image;
            image.alt = options.title || "NCERC campus facility";
            image.className = "facility-image";
            image.loading = "lazy";
            image.decoding = "async";
            image.width = 220;
            image.height = 140;
            image.onerror = () => image.remove();
            message.appendChild(image);
        }

        if (options.link) {
            const link = document.createElement("a");
            link.href = options.link;
            link.textContent = options.linkText || "Open link";
            link.target = "_blank";
            link.rel = "noopener noreferrer";
            link.className = "message-link";
            message.appendChild(link);
        }

        if (Array.isArray(options.suggestions) && options.suggestions.length) {
            const suggestions = document.createElement("div");
            suggestions.className = "message-suggestions";

            const label = document.createElement("span");
            label.textContent = "You could also ask:";
            suggestions.appendChild(label);

            options.suggestions.forEach(({ label: suggestionLabel, question }) => {
                const button = document.createElement("button");
                button.type = "button";
                button.className = "suggestion";
                button.dataset.question = question;
                button.textContent = suggestionLabel;
                suggestions.appendChild(button);
            });

            message.appendChild(suggestions);
        }

        if (sender === "bot" && options.feedbackQuestion) {
            const feedback = document.createElement("div");
            feedback.className = "message-feedback";
            feedback.setAttribute("role", "group");
            feedback.setAttribute("aria-label", "Rate this answer");

            const label = document.createElement("span");
            label.textContent = "Was this helpful?";
            feedback.appendChild(label);

            [
                { value: true, text: "👍 Helpful" },
                { value: false, text: "👎 Not helpful" }
            ].forEach(({ value, text }) => {
                const button = document.createElement("button");
                button.type = "button";
                button.textContent = text;
                button.addEventListener("click", () =>
                    submitFeedback(button, feedback, options.feedbackQuestion, value)
                );
                feedback.appendChild(button);
            });

            message.appendChild(feedback);
        }

        chatMessages.appendChild(message);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function getCookie(name) {
        const cookie = document.cookie
            .split("; ")
            .find((part) => part.startsWith(`${name}=`));

        return cookie ? decodeURIComponent(cookie.slice(name.length + 1)) : "";
    }

    async function submitFeedback(button, container, question, isHelpful) {
        const buttons = container.querySelectorAll("button");
        buttons.forEach((item) => {
            item.disabled = true;
        });

        try {
            const response = await fetch("/api/feedback/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    question,
                    is_helpful: isHelpful
                })
            });
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || "Feedback could not be saved.");
            }

            const status = document.createElement("span");
            status.className = "feedback-status";
            status.setAttribute("role", "status");
            status.textContent = "Thanks for your feedback.";
            container.replaceChildren(status);
        } catch (error) {
            console.error("Could not save chatbot feedback:", error);
            buttons.forEach((item) => {
                item.disabled = false;
            });
            button.setAttribute(
                "aria-label",
                error.message || "Feedback could not be saved. Please try again."
            );
            const status = container.querySelector(".feedback-status");

            if (status) {
                status.textContent = "Feedback could not be saved. Please try again.";
            } else {
                const errorStatus = document.createElement("span");
                errorStatus.className = "feedback-status";
                errorStatus.setAttribute("role", "alert");
                errorStatus.textContent =
                    "Feedback could not be saved. Please try again.";
                container.appendChild(errorStatus);
            }
        }
    }

    function showTyping(show) {
        if (typingIndicator) {
            typingIndicator.style.display = show ? "block" : "none";
        }

        if (askButton) {
            askButton.disabled = show;
        }
    }

    // ==============================
    // FACILITIES
    // ==============================

    const places = [
        {
            names: ["library", "central library"],
            dataKey: "library",
            image: "/static/helpdesk/images/optimized/library.jpg"
        },
        {
            names: ["fitness centre", "fitness center", "gym"],
            dataKey: "fitness_centre",
            image: "/static/helpdesk/images/optimized/gym.jpg"
        },
        {
            names: ["canteen", "cafeteria", "food"],
            dataKey: "canteen",
            image: "/static/helpdesk/images/optimized/canteen.jpg"
        },
        {
            names: [
                "transportation",
                "college bus",
                "college buses",
                "bus service"
            ],
            dataKey: "transportation",
            image: "/static/helpdesk/images/optimized/transport.jpg"
        },
        {
            names: ["hostel", "hostels"],
            title: "NCERC Hostels",
            dataKey: "hostels",
            answer:
                "NCERC provides separate hostel accommodation for boys and girls (Kasturba Ladies Hostel, Men's Hostel with sports and Wi-Fi, Priyadarshini block, and Kamala hostel).",
            location: { facility: "NCERC Hostels", location: "NCERC Campus" },
            image: "/static/helpdesk/images/optimized/hostel.jpg"
        },
        {
            names: ["seminar hall"],
            title: "Seminar Hall",
            answer:
                "The seminar hall is used for seminars, presentations and academic events. Contact the college for its exact location and availability.",
            location: {},
            image: "/static/helpdesk/images/optimized/seminar hall.jpg"
        },
        {
            names: ["auditorium", "audi", "main auditorium"],
            title: "NCERC Main Auditorium",
            dataKey: "auditorium",
            answer:
                "The Main Auditorium is situated on the second floor of Brahmagupta Block with an 800-seat capacity.",
            location: { facility: "NCERC Main Auditorium", block: "Brahmagupta Block", floor: "Second Floor" },
            image: "/static/helpdesk/images/optimized/auditorium.jpg"
        },
        {
            names: ["playground", "play ground", "sports ground", "athletic field", "outdoor sports"],
            title: "Playground & Outdoor Sports Facilities",
            dataKey: "sports_playground",
            answer:
                "The NCERC playground and outdoor sports facilities are located on the campus grounds for football, cricket, basketball, volleyball, and athletics.",
            location: { facility: "Playground & Outdoor Sports Facilities", location: "NCERC Campus Grounds" }
        },
        {
            names: ["basketball", "basketball court", "basket ball"],
            title: "Basketball Court",
            dataKey: "basketball_court",
            answer:
                "The basketball court is an outdoor court located on the NCERC campus grounds as part of the college's sports and games facilities.",
            location: { facility: "Basketball Court", location: "NCERC Campus Grounds" }
        },
        {
            names: ["kapila", "kapila block", "kapila building"],
            title: "Kapila Block",
            dataKey: "kapila_block",
            answer:
                "Kapila Block (60,000 sq. ft.) houses the MBA and MCA Departments, PG library, board room, tutorial rooms, classrooms, seminar halls, yoga hall, and computer laboratories.",
            location: { facility: "Kapila Block", block: "Kapila Block" }
        },
        {
            names: ["varahamihira", "varahamihira block", "varahmihira"],
            title: "Varahamihira Block",
            dataKey: "varahamihira_block",
            answer:
                "Varahamihira Block (30,000 sq. ft.) is the main workshop building housing 12 Mechanical Engineering workshops, 3 Electrical Engineering laboratories, and a Civil Engineering lab.",
            location: { facility: "Varahamihira Block", block: "Varahamihira Block" }
        },
        {
            names: ["brahmagupta", "brahmagupta block"],
            title: "Brahmagupta Block",
            dataKey: "brahmagupta_block",
            answer:
                "Brahmagupta Block houses the Central Library on the ground floor, the Main Auditorium on the second floor, an automobile workshop, and an electronics laboratory.",
            location: { facility: "Brahmagupta Block", block: "Brahmagupta Block" }
        },
        {
            names: ["administrative office", "admin office", "administration office", "college office"],
            title: "Administrative & Academic Offices",
            dataKey: "administrative_office",
            answer:
                "The Academic Office and Principal's Office are situated on the First Floor of Aryabhatta Block. General administrative assistance is available through reception or office@ncerc.ac.in.",
            location: { facility: "Administrative & Academic Offices", block: "Aryabhatta Block", floor: "First Floor" }
        }
    ];

    function getPlaceLocation(placeData) {
        const location = {};
        if (placeData && placeData.block) {
            location.block = placeData.block;
        }
        if (placeData && placeData.floor) {
            location.floor = placeData.floor;
        }
        const locationText =
            placeData && typeof placeData.location === "string"
                ? placeData.location
                : "";

        if (locationText) {
            const blockMatch = locationText.match(
                /\b(Bhaskara|Brahmagupta|Aryabhatta|Kapila|Varahamihira)\s+block\b/i
            );
            const floorMatch = locationText.match(
                /\b(ground|basement|first|second|third|fourth)(?:\s+floor)?\b/i
            );

            if (blockMatch && !location.block) {
                location.block = `${blockMatch[1]} Block`;
            }

            if (floorMatch && !location.floor) {
                location.floor =
                    `${floorMatch[1].charAt(0).toUpperCase()}${floorMatch[1].slice(1)} Floor`;
            }

            if (!blockMatch && !floorMatch && !location.block && !location.floor) {
                location.location = locationText;
            }
        }

        if (placeData && placeData.timing) {
            location.timing = placeData.timing;
        }

        return location;
    }

    function getPlaceAnswer(place) {
        const placeData =
            place.dataKey && ncercData[place.dataKey]
                ? ncercData[place.dataKey]
                : null;
        const title = (placeData && placeData.name) || place.title;
        const details = [];

        if (placeData && placeData.description) {
            details.push(placeData.description);
        } else if (place.answer) {
            details.push(place.answer);
        }

        if (!placeData || !placeData.location) {
            if (placeData && placeData.timing) {
                details.push("Location details are not listed in the available campus data.");
            } else if (placeData) {
                details.push(
                    "Location and timings are not listed in the available campus data."
                );
            }
        }

        return {
            text: [title, ...details].join("\n"),
            image: place.image,
            title,
            location: {
                facility: title,
                ...getPlaceLocation(placeData)
            },
            links: [
                { href: tourUrl, label: "Explore Campus in 360°" },
                { href: campusMapUrl, label: "Open Campus Map" }
            ]
        };
    }

    // ==============================
    // DEPARTMENTS
    // ==============================

    const departments = [
        {
            names: [
                "computer science and engineering",
                "computer science",
                "cse"
            ],
            title: "Computer Science and Engineering",
            answer:
                "The Computer Science and Engineering (CSE) department focuses on computing, programming, algorithms and software development."
        },
        {
            names: [
                "artificial intelligence machine learning",
                "artificial intelligence",
                "machine learning",
                "aiml"
            ],
            title: "Artificial Intelligence and Machine Learning",
            answer:
                "The Artificial Intelligence and Machine Learning department focuses on AI methods, machine learning, intelligent systems and data-driven applications."
        },
        {
            names: [
                "electronics and communication",
                "electronics communication",
                "ece"
            ],
            title: "Electronics and Communication Engineering",
            answer:
                "The Electronics and Communication Engineering (ECE) department covers electronic systems, communication and related engineering technologies."
        },
        {
            names: [
                "electrical and electronics",
                "electrical electronics",
                "eee"
            ],
            title: "Electrical and Electronics Engineering",
            answer:
                "The Electrical and Electronics Engineering (EEE) department covers electrical systems, electronics, power and related engineering subjects."
        },
        {
            names: ["mechanical engineering", "mechanical"],
            title: "Mechanical Engineering",
            answer:
                "The Mechanical Engineering department covers mechanical systems, design, manufacturing and related engineering principles."
        },
        {
            names: ["mechatronics"],
            title: "Mechatronics Engineering",
            answer:
                "Mechatronics combines mechanical engineering, electronics, control systems and automation."
        }
    ];

    function containsPhrase(question, phrase) {
        return normalize(question).includes(normalize(phrase));
    }

    // ==============================
    // ROOM AND BLOCK SEARCH
    // ==============================

    function findCampusLocations(originalQuestion) {
        const question = expandQuestion(originalQuestion);

        const roomMatch = question.match(
            /\b(?:room\s*)?(\d{3}[a-z]?)\b/i
        );

        const requestedRoom = roomMatch
            ? roomMatch[1].toLowerCase()
            : null;

        const results = [];

        function matchesLocationText(text, sectionName) {
            const searchableText = normalize(`${sectionName} ${text}`);

            if (question.includes(normalize(text))) {
                return true;
            }

            const ignoredWords = new Set([
                "about",
                "are",
                "find",
                "floor",
                "for",
                "in",
                "is",
                "location",
                "me",
                "of",
                "on",
                "room",
                "the",
                "where",
                "which"
            ]);
            const queryWords = question
                .split(/\s+/)
                .filter((word) => word.length > 1 && !ignoredWords.has(word));
            const searchableWords = new Set(searchableText.split(/\s+/));

            return (
                queryWords.length > 0 &&
                queryWords.every((word) => searchableWords.has(word))
            );
        }

        function roomKeyMatches(key, room) {
            if (key.toLowerCase() === room) {
                return true;
            }

            const rangeMatch = key.match(/^(\d{3})\s*-\s*(\d{3})$/);

            if (!rangeMatch || /[a-z]/i.test(room)) {
                return false;
            }

            const roomNumber = Number(room);
            return (
                roomNumber >= Number(rangeMatch[1]) &&
                roomNumber <= Number(rangeMatch[2])
            );
        }

        function inspectData(
            value,
            path = "",
            depth = 0,
            sectionName = "",
            parentField = ""
        ) {
            if (depth > 8 || value == null) return;

            if (
                typeof value === "string" ||
                typeof value === "number"
            ) {
                const text = String(value);
                const normalizedValue = normalize(text);

                if (
                    !requestedRoom &&
                    normalizedValue &&
                    matchesLocationText(text, sectionName)
                ) {
                    const roomNumber =
                        parentField === "rooms" ||
                        parentField === "room_ranges"
                            ? path.split(" / ").pop()
                            : "";

                    results.push({
                        title: sectionName || path || "Campus location",
                        detail: roomNumber
                            ? `${parentField === "room_ranges" ? "Rooms" : "Room"} ${roomNumber}: ${text}`
                            : text
                    });
                }

                return;
            }

            if (Array.isArray(value)) {
                value.forEach((item, index) => {
                    inspectData(
                        item,
                        `${path} ${index + 1}`.trim(),
                        depth + 1,
                        sectionName,
                        parentField
                    );
                });
                return;
            }

            if (typeof value === "object") {
                const currentSectionName =
                    typeof value.name === "string"
                        ? value.name
                        : sectionName;

                for (const [key, item] of Object.entries(value)) {
                    const nextPath = path
                        ? `${path} / ${key}`
                        : key;

                    if (
                        requestedRoom &&
                        (parentField === "rooms" ||
                            parentField === "room_ranges") &&
                        roomKeyMatches(key, requestedRoom)
                    ) {
                        const isRange = key.includes("-");
                        const roomLabel = isRange
                            ? `Room ${requestedRoom.toUpperCase()} (within ${key})`
                            : `Room ${key.toUpperCase()}`;

                        results.push({
                            title: currentSectionName || path || "Campus location",
                            detail: `${roomLabel}: ${item}`
                        });
                    }

                    inspectData(
                        item,
                        nextPath,
                        depth + 1,
                        currentSectionName,
                        key
                    );
                }
            }
        }

        inspectData(ncercData);

        const uniqueResults = [];
        const seen = new Set();

        for (const result of results) {
            const key = `${result.title}|${result.detail}`;

            if (!seen.has(key)) {
                seen.add(key);
                uniqueResults.push(result);
            }
        }

        return uniqueResults.slice(0, 5);
    }

    // Extract location details from a matched room-data record.
    // Only display a field when it is explicitly present in the data.
    function extractLocationDetails(result) {
        const combined = `${result.title} ${result.detail}`;
        const location = {};

        const blockMatch = combined.match(
            /\b(Bhaskara|Brahmagupta|Aryabhatta)\s*Block\b/i
        );

        if (blockMatch) {
            const name = blockMatch[1];
            location.block =
                name.charAt(0).toUpperCase() +
                name.slice(1).toLowerCase() +
                " Block";
        }

        const floorPatterns = [
            {
                regex: /\b(?:ground|ground floor)\b/i,
                value: "Ground Floor"
            },
            {
                regex: /\b(?:basement|basement floor)\b/i,
                value: "Basement Floor"
            },
            {
                regex: /\bfirst floor\b/i,
                value: "First Floor"
            },
            {
                regex: /\bsecond floor\b/i,
                value: "Second Floor"
            },
            {
                regex: /\bthird floor\b/i,
                value: "Third Floor"
            },
            {
                regex: /\bfourth floor\b/i,
                value: "Fourth Floor"
            }
        ];

        const floorMatch = floorPatterns.find((item) =>
            item.regex.test(combined)
        );

        if (floorMatch) {
            location.floor = floorMatch.value;
        }

        const roomMatch = combined.match(
            /\broom\s*(\d{3}[a-z]?)\b/i
        );

        if (roomMatch) {
            location.room = roomMatch[1].toUpperCase();
        } else {
            const numberInQuestion = normalize(result.detail).match(
                /\b(\d{3}[a-z]?)\b/i
            );

            if (numberInQuestion) {
                location.room = numberInQuestion[1].toUpperCase();
            }
        }

        return location;
    }

    function findAryabhattaFloor(question) {
        if (!question.includes("aryabhatta")) {
            return null;
        }

        const floorMatch = question.match(
            /\b(ground|first|second|third|fourth|1st|2nd|3rd|4th)\s+floor\b/
        );

        if (!floorMatch) {
            return null;
        }

        const floorNames = {
            ground: "Ground",
            first: "First",
            second: "Second",
            third: "Third",
            fourth: "Fourth",
            "1st": "First",
            "2nd": "Second",
            "3rd": "Third",
            "4th": "Fourth"
        };
        const floorName = `${floorNames[floorMatch[1]]} floor`;
        const floorData = Object.values(ncercData).find(
            (item) =>
                item &&
                typeof item === "object" &&
                typeof item.name === "string" &&
                normalize(item.name).includes(
                    normalize(`Aryabhatta Block - ${floorName}`)
                )
        );

        if (!floorData) {
            return null;
        }

        const details = [];

        if (floorData.rooms) {
            details.push(
                ...Object.entries(floorData.rooms).map(
                    ([room, description]) => `Room ${room}: ${description}`
                )
            );
        }

        if (floorData.room_ranges) {
            details.push(
                ...Object.entries(floorData.room_ranges).map(
                    ([rooms, description]) => `Rooms ${rooms}: ${description}`
                )
            );
        }

        if (floorData.facilities) {
            details.push(...floorData.facilities);
        }

        return {
            text: `${floorData.name}\n\n${details.join("\n")}`,
            floor: `${floorNames[floorMatch[1]]} Floor`
        };
    }

    function getRelatedSuggestions(question) {
        return /\b(room|block|floor|lab|office|cabin|classroom|toilet)\b/i.test(question)
            ? [
                { label: "Find room 318", question: "Where is room 318?" },
                { label: "Browse Aryabhatta floors", question: "What is on Aryabhatta first floor?" },
                { label: "Browse facilities", question: "What facilities are available?" }
            ]
            : [
                { label: "Library", question: "Where is the library?" },
                { label: "Canteen", question: "What are the canteen timings?" },
                { label: "Departments", question: "List all departments." },
                { label: "Campus Tour", question: "Show me the campus tour." }
            ];
    }

    // ==============================
    // ANSWER RULES
    // ==============================

    function getAnswer(originalQuestion) {
        const question = expandQuestion(originalQuestion);
        const locationIntent =
            /\b(?:where is|where are|where can i find|where can i locate|location of|how can i reach|how do i get to|how to reach|directions to|show me where)\b/i.test(
                normalize(originalQuestion)
            );

        if (!question) {
            return {
                text: "Please type a question about NCERC, such as a room number, department, facility or campus location."
            };
        }

        // Greetings
        if (
            /^(hi|hello|hey|good morning|good afternoon|good evening)\b/.test(
                question
            )
        ) {
            return {
                text: "Hello! 👋 Welcome to the NCERC Helpdesk. Ask me about facilities, departments, rooms, timings or campus navigation."
            };
        }

        // Thanks
        if (
            question.includes("thank you") ||
            question === "thanks" ||
            question.startsWith("thanks ")
        ) {
            return {
                text: "You're welcome! 😊 Feel free to ask if you need more information about NCERC."
            };
        }

        // Identity
        if (
            question.includes("who are you") ||
            question.includes("what are you") ||
            question.includes("your name")
        ) {
            return {
                text: "I am the NCERC Helpdesk Assistant. I provide rule-based campus information using the data available in this project."
            };
        }

        // Capabilities
        if (
            question.includes("what can you do") ||
            question.includes("what do you know") ||
            question.includes("help me")
        ) {
            return {
                text:
                    "I can help with:\n\n" +
                    "📚 Library information\n" +
                    "💪 Fitness Centre location\n" +
                    "🍽️ Canteen timings\n" +
                    "🚌 College transportation\n" +
                    "🏫 Department information\n" +
                    "🚪 Room and block searches using available campus data\n" +
                    "🧭 NCERC virtual campus tour\n\n" +
                    "Ask a question in your own words."
            };
        }

        // Campus map
        if (
            question === "map" ||
            question.includes("campus map") ||
            question.includes("google map") ||
            question.includes("open map") ||
            question.includes("directions to campus")
        ) {
            return {
                text:
                    "Use Google Maps to find NCERC and get directions to the campus. " +
                    "Building-to-building routes are not available in the supplied campus data.",
                links: [
                    { href: campusMapUrl, label: "Open Campus Map" },
                    { href: tourUrl, label: "Explore Campus in 360°" }
                ]
            };
        }

        // Campus tour
        if (
            question.includes("360") ||
            question.includes("virtual tour") ||
            question.includes("campus tour") ||
            question.includes("explore campus") ||
            question.includes("explore the campus") ||
            question.includes("campus navigation") ||
            question.includes("navigate campus")
        ) {
            return {
                text: "Explore the NCERC campus through the official 360° virtual tour.",
                links: [
                    { href: tourUrl, label: "Explore Campus in 360°" },
                    { href: campusMapUrl, label: "Open Campus Map" }
                ]
            };
        }

        // List facilities
        if (
            question.includes("what facilities") ||
            question.includes("available facilities") ||
            question.includes("facilities available") ||
            question.includes("facilities in college") ||
            question.includes("facilities does ncerc") ||
            question === "facilities"
        ) {
            return {
                text:
                    "Here are some NCERC facilities covered by this helpdesk:\n\n" +
                    "📚 Central Library — Brahmagupta Block, Ground Floor\n" +
                    "🍽️ Canteen — 8:00 AM to 5:00 PM on working days, including Saturday\n" +
                    "💪 Fitness Centre — Bhaskara Block, Basement Floor\n" +
                    "🚌 College Transportation — bus services for students and staff\n\n" +
                    "Ask about a facility for more details."
            };
        }

        // Helpdesk instructions
        if (
            question.includes("how do i use this helpdesk") ||
            question.includes("how to use this helpdesk") ||
            question.includes("how does this helpdesk work") ||
            question.includes("how can i use this")
        ) {
            return {
                text:
                    "Using the NCERC Helpdesk is simple:\n\n" +
                    "1. Type your question in the chat box.\n" +
                    "2. Press Send.\n" +
                    "3. Read the answer and open any link provided.\n" +
                    "4. Ask another question when needed.\n\n" +
                    "You can ask about facilities, departments, rooms, timings and campus navigation."
            };
        }

        const aryabhattaFloorInformation = findAryabhattaFloor(question);

        if (aryabhattaFloorInformation) {
            return {
                text: aryabhattaFloorInformation.text,
                location: {
                    block: "Aryabhatta Block",
                    floor: aryabhattaFloorInformation.floor
                },
                links: [
                    { href: tourUrl, label: "Explore Campus in 360°" },
                    { href: campusMapUrl, label: "Open Campus Map" }
                ]
            };
        }

        // Room or block search
        const roomRequested =
            /\broom\s*\d{3}[a-z]?\b/i.test(question) ||
            /\b\d{3}[a-z]?\b/i.test(question) ||
            question.includes("room location") ||
            question.includes("which room") ||
            question.includes("bhaskara block") ||
            question.includes("aryabhatta block") ||
            question.includes("brahmagupta block") ||
            /\b(?:floor|classroom|lab|toilet|office|cabin|common room|tutorial room|seminar hall|conference room|dining room|sick room|fire exit|emergency exit)\b/i.test(question);

        if (roomRequested) {
            const locations = findCampusLocations(originalQuestion);

            if (locations.length > 0) {
                return {
                    text:
                        "I found the following matching campus information:\n\n" +
                        locations.map((item, index) =>
                            `${index + 1}. ${item.title}\n${item.detail}`
                        ).join("\n\n") +
                        "\n\nPlease confirm the location with the college if you need an official room assignment.",
                    location: extractLocationDetails(locations[0]),
                    links: [
                        { href: tourUrl, label: "Explore Campus in 360°" },
                        { href: campusMapUrl, label: "Open Campus Map" }
                    ]
                };
            }

            // Answer known block queries without inventing a room number.
            if (question.includes("bhaskara block")) {
                return {
                    text: "The Fitness Centre is located in the basement of the Bhaskara Block. For other rooms, please check the available campus data or contact the college office.",
                    location: {
                        block: "Bhaskara Block",
                        floor: "Basement Floor"
                    },
                    image: "/static/helpdesk/images/optimized/gym.jpg",
                    title: "Bhaskara Block",
                    links: [
                        { href: tourUrl, label: "Explore Campus in 360°" },
                        { href: campusMapUrl, label: "Open Campus Map" }
                    ]
                };
            }

            return {
                text: "I couldn't find an exact match in the campus data currently loaded into this helpdesk. Please check the room number and block name, or consult the college office.",
                suggestions: getRelatedSuggestions(question)
            };
        }

        // Department list
        if (
            question.includes("list departments") ||
            question.includes("all departments") ||
            question.includes("departments in ncerc") ||
            question.includes("departments available") ||
            question === "departments"
        ) {
            return {
                text:
                    "The departments covered by this helpdesk include:\n\n" +
                    departments.map((department, index) =>
                        `${index + 1}. ${department.title}`
                    ).join("\n") +
                    "\n\nAsk about a specific department for more information."
            };
        }

        // Specific department
        const matchedDepartment = departments.find((department) =>
            department.names.some((name) =>
                containsPhrase(question, name)
            )
        );

        if (matchedDepartment) {
            if (locationIntent) {
                return {
                    text:
                        `I don't have a verified campus location for ${matchedDepartment.title} ` +
                        "in the available college data. Please confirm the location with college staff.",
                    title: matchedDepartment.title,
                    links: [
                        { href: tourUrl, label: "Explore Campus in 360°" },
                        { href: campusMapUrl, label: "Open Campus Map" }
                    ]
                };
            }

            return {
                text: matchedDepartment.answer,
                title: matchedDepartment.title
            };
        }

        // Specific facility
        const matchedPlace = places.find((place) =>
            place.names.some((name) =>
                containsPhrase(question, name)
            )
        );

        if (matchedPlace) {
            return getPlaceAnswer(matchedPlace);
        }

        if (locationIntent) {
            const locations = findCampusLocations(originalQuestion);

            if (locations.length > 0) {
                return {
                    text:
                        "I found the following matching campus information:\n\n" +
                        locations.map((item, index) =>
                            `${index + 1}. ${item.title}\n${item.detail}`
                        ).join("\n\n") +
                        "\n\nPlease confirm the location with the college if you need an official assignment.",
                    location: extractLocationDetails(locations[0]),
                    links: [
                        { href: tourUrl, label: "Explore Campus in 360°" },
                        { href: campusMapUrl, label: "Open Campus Map" }
                    ]
                };
            }
        }

        // General college information
        if (
            question.includes("ncerc") ||
            question.includes("college information") ||
            question.includes("about the college")
        ) {
            return {
                text:
                    "This helpdesk provides basic NCERC campus information. " +
                    "Ask about the Central Library, Canteen, Fitness Centre, transportation, " +
                    "departments, room locations in the loaded data, or the 360° campus tour."
            };
        }

        // Fallback
        return {
            text:
                "I couldn't match that question to the campus information I have. " +
                "Try one of these related questions, or ask about a room, facility, department, or campus tour.",
            suggestions: getRelatedSuggestions(question)
        };
    }

    // ==============================
    // SEND QUESTION
    // ==============================

    async function requestAIAnswer(question) {
        const response = await fetch("/api/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ message: question })
        });
        const result = await response.json();

        if (!response.ok || result.fallback) {
            throw new Error(result.error || "The AI model is unavailable.");
        }

        return {
            text: result.answer,
            title: result.title,
            image: result.image,
            location: result.location,
            links: result.links,
            mode: result.mode,
            provider: result.provider
        };
    }

    async function sendQuestion(questionText) {
        const question = String(questionText || "").trim();

        if (!question) {
            if (questionInput) questionInput.focus();
            return;
        }

        addMessage(question, "user");

        if (questionInput) {
            questionInput.value = "";
        }

        showTyping(true);

        try {
            let answer;
            let mode = "ai";
            let provider = null;
            try {
                answer = await requestAIAnswer(question);
                mode = answer.mode || "ai";
                provider = answer.provider || null;
            } catch (error) {
                console.warn("AI chat unavailable; using local rules:", error.message);
                answer = getAnswer(question);
                answer.text =
                    "The AI assistant is unavailable, so I used the local helpdesk rules.\n\n" +
                    answer.text;
                mode = "fallback";
            }

            addMessage(answer.text, "bot", {
                image: answer.image,
                title: answer.title,
                link: answer.link,
                linkText: answer.linkText,
                links: answer.links,
                location: answer.location,
                suggestions: answer.suggestions,
                feedbackQuestion: question,
                mode,
                provider
            });
        } catch (error) {
            console.error("Helpdesk error:", error);
            addMessage(
                "Sorry, I couldn't process that question. Please try asking it in a different way.",
                "bot"
            );
        } finally {
            showTyping(false);

            if (questionInput) {
                questionInput.focus();
            }
        }
    }

    // Form submission
    if (chatForm) {
        chatForm.addEventListener("submit", (event) => {
            event.preventDefault();
            sendQuestion(questionInput ? questionInput.value : "");
        });
    }

    // Suggested questions, including suggestions added to answers.
    document.addEventListener("click", (event) => {
        const button = event.target.closest("[data-question], .suggestion-btn");

        if (!button) return;

        const suggestedQuestion =
            button.dataset.question ||
            button.textContent.trim();

        sendQuestion(suggestedQuestion);
    });

    console.log("NCERC AI chat with local rule-based fallback is ready.");
});
