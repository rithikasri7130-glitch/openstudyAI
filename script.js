const pdfInput = document.getElementById("pdf");
const filenameEl = document.getElementById("filename");
const questionEl = document.getElementById("question");
const responseEl = document.getElementById("response");

pdfInput.addEventListener("change", () => {
  filenameEl.textContent = pdfInput.files[0]
    ? "Selected: " + pdfInput.files[0].name
    : "No file selected";
});

async function send(mode) {
  const question = questionEl.value.trim();
  const file = pdfInput.files[0];

  if (mode === "ask" && !question) {
    responseEl.innerText = "Question type pannu.";
    return;
  }

  responseEl.innerText = "AI yosikkuthu... wait pannu ⏳";

  const fd = new FormData();
  fd.append("mode", mode);
  fd.append("question", question);
  if (file) fd.append("pdf", file);

  try {
    const res = await fetch("/api/study", { method: "POST", body: fd });
    const data = await res.json();
    responseEl.innerText = data.answer || data.error || "No response";
  } catch (e) {
    responseEl.innerText = "Server error: " + e.message;
  }
}

document.getElementById("ask").addEventListener("click", () => send("ask"));
document.getElementById("summary").addEventListener("click", () => send("summary"));
document.getElementById("quiz").addEventListener("click", () => send("quiz"));

 
    


 

  