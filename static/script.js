console.log("JS loaded");

function generate() {
  const subject = document.getElementById("subject").value;
  const topic = document.getElementById("topic").value;
  const type = document.getElementById("type").value;

  const outputDiv = document.getElementById("output");
  outputDiv.innerHTML = "Generating... ⏳";

  fetch("/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      subject: subject,
      topic: topic,
      type: type
    })
  })
    .then(res => res.json())
    .then(data => {
      console.log("Backend response:", data);

      // 🔒 Safety check
      if (!data || (!data.output && !data.error)) {
        outputDiv.innerHTML = "No output received from AI.";
        return;
      }

      // ❌ Backend error
      if (data.error) {
        outputDiv.innerHTML = "Backend Error: " + data.error;
        return;
      }

      // 🧠 QUIZ MODE
      if (type === "quiz") {
        renderQuiz(data.output);
        return;
      }

      // 📄 NORMAL TEXT MODE
      outputDiv.innerHTML = data.output
        ? data.output.replace(/\n/g, "<br>")
        : "No output received from AI.";
    })
    .catch(err => {
      outputDiv.innerHTML = "Frontend Error. Check console.";
      console.error("Frontend error:", err);
    });
}

function renderQuiz(rawText) {
  const outputDiv = document.getElementById("output");
  outputDiv.innerHTML = "";

  // 🔒 Safety check
  if (!rawText || typeof rawText !== "string") {
    outputDiv.innerHTML = "No quiz content received.";
    return;
  }

  const blocks = rawText.split("\n\n");

  blocks.forEach(block => {
    const lines = block
      .split("\n")
      .map(l => l.trim())
      .filter(l => l !== "");

    if (lines.length < 6) return; // skip invalid blocks

    const question = lines[0];
    const options = lines.slice(1, 5);

    const answerLine = lines.find(l => l.startsWith("Answer:"));
    if (!answerLine) return;

    const correct = answerLine.split(":")[1].trim();

    const qDiv = document.createElement("div");
    qDiv.className = "question";

    const qTitle = document.createElement("h3");
    qTitle.innerText = question;
    qDiv.appendChild(qTitle);

    options.forEach(opt => {
      const btn = document.createElement("button");
      btn.className = "option-btn";
      btn.innerText = opt;

      btn.onclick = () => {
        // Disable all buttons after click
        qDiv.querySelectorAll("button").forEach(b => b.disabled = true);

        if (opt.startsWith(correct)) {
          btn.classList.add("correct");
        } else {
          btn.classList.add("wrong");
        }
      };

      qDiv.appendChild(btn);
    });

    outputDiv.appendChild(qDiv);
  });
}
