function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toUTCString().replace("GMT", "UTC");
}

async function fetchEvents() {
  const res = await fetch("http://localhost:5000/events");
  const events = await res.json();

  const list = document.getElementById("events");
  list.innerHTML = "";

  events.forEach(e => {
    let text = "";

    if (e.type === "PUSH") {
      text = `${e.author} pushed to ${e.to_branch} on ${formatDate(e.timestamp)}`;
    }

    if (e.type === "PULL_REQUEST") {
      text = `${e.author} submitted a pull request from ${e.from_branch} to ${e.to_branch} on ${formatDate(e.timestamp)}`;
    }

    if (e.type === "MERGE") {
      text = `${e.author} merged branch ${e.from_branch} to ${e.to_branch} on ${formatDate(e.timestamp)}`;
    }

    const li = document.createElement("li");
    li.textContent = text;
    list.appendChild(li);
  });
}

fetchEvents();
setInterval(fetchEvents, 15000);
