document.getElementById("send").onclick = async () => {
  const q = document.getElementById("query").value;
  if (!q) return;

  const context = {
    tdrop: 28,
    tbar: 1013,
    tskinice: 25,
    rainocn: 0.3,
    delts: 0.5,
    latitude: 15.0,
    longitude: 75.0
  };

  const hist = document.getElementById("history");
  hist.innerHTML += `<div class="user">You: ${q}</div>`;
  document.getElementById("query").value = "";

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
    hist.innerHTML += `<div class="bot">Neptune: ${data.response}</div>`;
  } catch (error) {
    console.error("Error sending message:", error);
    hist.innerHTML += `<div class="bot error">Neptune: Sorry, an error occurred. Please try again.</div>`;
  }

  hist.scrollTop = hist.scrollHeight;
};
