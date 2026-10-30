// NCERC COLLEGE HELPDESK

function askQuestion() {
    const input = document.getElementById("question");
    const answer = document.getElementById("answer");

    if (!input || !answer) {
        alert("Question input or answer area is missing.");
        return;
    }

    const question = input.value.toLowerCase().trim();

    if (question === "") {
        answer.textContent = "Please enter a question about NCERC.";
        return;
    }

    let data = {};

    const dataElement = document.getElementById("ncerc-data");

    if (dataElement) {
        try {
            data = JSON.parse(dataElement.textContent);
        } catch (error) {
            console.error("College data error:", error);
        }
    }

    // LIBRARY
    if (
        question.includes("library") ||
        question.includes("books") ||
        question.includes("journals")
    ) {
        answer.innerHTML =
            "<strong>📚 NCERC Central Library</strong><br><br>" +
            "<strong>Location:</strong> Ground Floor, Brahmagupta Block<br><br>" +
            (data.library?.description ||
                "The library provides books, journals and digital information services.");
    }

    // CANTEEN
    else if (
        question.includes("canteen") ||
        question.includes("food") ||
        question.includes("eat")
    ) {
        answer.innerHTML =
            "<strong>🍽️ NCERC Canteen</strong><br><br>" +
            "<strong>Location:</strong> Campus<br>" +
            "<strong>Timings:</strong> " +
            (data.canteen?.timing ||
                "8:00 AM to 5:00 PM on working days, including Saturday") +
            "<br><br>" +
            (data.canteen?.description ||
                "Food and refreshments for students and staff.");
    }

    // FITNESS CENTRE
    else if (
        question.includes("gym") ||
        question.includes("fitness") ||
        question.includes("exercise")
    ) {
        answer.innerHTML =
            "<strong>💪 Fitness Centre</strong><br><br>" +
            "<strong>Location:</strong> Bhaskara Building<br><br>" +
            (data.fitness_centre?.description ||
                "The fitness centre has gym equipment for students and staff.");
    }

    // TRANSPORTATION
    else if (
        question.includes("transport") ||
        question.includes("bus") ||
        question.includes("travel")
    ) {
        answer.innerHTML =
            "<strong>🚌 College Transportation</strong><br><br>" +
            (data.transportation?.description ||
                "NCERC provides transportation for students and staff through college buses.");
    }

    // MECHATRONICS — BEFORE MECHANICAL
    else if (
        question.includes("mechatronics") ||
        /\bmtr\b/.test(question)
    ) {
        answer.innerHTML =
            "<strong>🤖 Department of Mechatronics Engineering (MTR)</strong><br><br>" +
            "<strong>Course:</strong> B.Tech Mechatronics Engineering.";
    }

    // AI AND MACHINE LEARNING
    else if (
        question.includes("artificial intelligence") ||
        question.includes("machine learning") ||
        question.includes("ai & ml") ||
        question.includes("ai and ml") ||
        question.includes("aiml")
    ) {
        answer.innerHTML =
            "<strong>🤖 Computer Science — AI &amp; ML</strong><br><br>" +
            "<strong>Course:</strong> B.Tech Computer Science and Engineering " +
            "(Artificial Intelligence &amp; Machine Learning).";
    }

    // ELECTRONICS AND COMMUNICATION
    else if (
        question.includes("ece") ||
        question.includes("electronics") ||
        question.includes("vlsi")
    ) {
        answer.innerHTML =
            "<strong>📡 Electronics and Communication Engineering</strong><br><br>" +
            "• B.Tech Electronics and Communication Engineering<br>" +
            "• M.Tech VLSI Design";
    }

    // ELECTRICAL AND ELECTRONICS
    else if (
        question.includes("electrical") ||
        /\beee\b/.test(question) ||
        question.includes("energy systems")
    ) {
        answer.innerHTML =
            "<strong>⚡ Electrical and Electronics Engineering</strong><br><br>" +
            "• B.Tech Electrical &amp; Computer Engineering<br>" +
            "• M.Tech Energy Systems";
    }

    // MECHANICAL
    else if (question.includes("mechanical")) {
        answer.innerHTML =
            "<strong>⚙️ Mechanical Engineering</strong><br><br>" +
            "Course: B.Tech Mechanical Engineering (Industry Integrated).";
    }

    // COMPUTER SCIENCE
    else if (
        question.includes("cse") ||
        question.includes("computer science") ||
        question.includes("computer engineering")
    ) {
        answer.innerHTML =
            "<strong>💻 Computer Science and Engineering</strong><br><br>" +
            "• B.Tech Computer Science and Engineering<br>" +
            "• M.Tech Computer Science and Engineering";
    }

    // ALL DEPARTMENTS
    else if (
        question.includes("department") ||
        question.includes("courses") ||
        question.includes("branches") ||
        question.includes("engineering")
    ) {
        answer.innerHTML =
            "<strong>🎓 NCERC Departments</strong><br><br>" +
            "• Computer Science and Engineering<br>" +
            "• Computer Science — AI &amp; ML<br>" +
            "• Electronics and Communication Engineering<br>" +
            "• Electrical and Electronics Engineering<br>" +
            "• Mechanical Engineering<br>" +
            "• Mechatronics Engineering (MTR)";
    }

    // UNKNOWN QUESTION
    else {
        answer.textContent =
            "Sorry, I don't have information about that yet. " +
            "Try asking about library, canteen, gym, buses, CSE, AI & ML, ECE, Mechanical, or MTR.";
    }
}

// CONNECT THE BUTTON AFTER THE PAGE LOADS
document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("ask-button");
    const input = document.getElementById("question");

    if (button) {
        button.addEventListener("click", askQuestion);
    }

    if (input) {
        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();
                askQuestion();
            }
        });
    }

    console.log("NCERC Helpdesk is ready.");
});