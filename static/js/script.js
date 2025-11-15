document.getElementById("send").onclick = async () => {
  const q = document.getElementById("query").value;
  if (!q.trim()) return;

  // Get context from input fields if they exist
  const context = {
    tdrop: parseFloat(document.getElementById("tdrop")?.value || 28),
    tbar: parseFloat(document.getElementById("tbar")?.value || 1013),
    tskinice: parseFloat(document.getElementById("tskinice")?.value || 25),
    rainocn: parseFloat(document.getElementById("rainocn")?.value || 0.3),
    delts: parseFloat(document.getElementById("delts")?.value || 0.5),
    latitude: parseFloat(document.getElementById("latitude")?.value || 15.0),
    longitude: parseFloat(document.getElementById("longitude")?.value || 75.0)
  };

  const hist = document.getElementById("history");
  
  // Add user message
  const userMsg = document.createElement("div");
  userMsg.className = "user";
  userMsg.textContent = "You: " + q;
  hist.appendChild(userMsg);
  
  document.getElementById("query").value = "";
  hist.scrollTop = hist.scrollHeight;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: q, context_data: context })
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    const data = await res.json();
    
    // Add bot response
    const botMsg = document.createElement("div");
    botMsg.className = "bot";
    botMsg.textContent = data.response || "No response received";
    hist.appendChild(botMsg);
    
  } catch (error) {
    console.error("Error sending message:", error);
    
    const errMsg = document.createElement("div");
    errMsg.className = "bot error";
    errMsg.textContent = "Neptune: Sorry, an error occurred. Please try again.";
    hist.appendChild(errMsg);
  }

  hist.scrollTop = hist.scrollHeight;
};

// Allow Enter key to send message
document.getElementById("query").addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    document.getElementById("send").click();
  }
});

