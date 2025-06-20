document.getElementById("msgForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const message = document.getElementById("message").value;
  const response = await fetch("/send/astro123", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  });

  const result = await response.json();
  const status = document.getElementById("status");

  if (result.status === "success") {
    status.innerText = "✅ Message sent!";
    document.getElementById("msgForm").reset();
  } else {
    status.innerText = "❌ Failed to send message.";
  }
});
