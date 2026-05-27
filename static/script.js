const form = document.getElementById("studentForm");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const data = {
        study_hours: document.getElementById("study_hours").value,
        social_media: document.getElementById("social_media").value,
        netflix: document.getElementById("netflix").value,
        attendance: document.getElementById("attendance").value,
        sleep: document.getElementById("sleep").value
    };

    const response = await fetch("/analyze", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)
    });

    const result = await response.json();

    document.getElementById("result").innerHTML = `

        <h2>AI Learning Insight</h2>

        <p>${result.insight}</p>

        <h2>Personalized Schedule</h2>

        <p>${result.schedule}</p>

    `;
});