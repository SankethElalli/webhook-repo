async function fetchEvents() {
  const res = await fetch("http://localhost:5000/events");
  const data = await res.json();

  const list = document.getElementById("events");
  list.innerHTML = "";

  data.forEach(event => {
    let text = "";

    if (event.type === "PUSH") {
      text = `${event.author} pushed to ${event.to_branch} on ${new Date(event.timestamp).toUTCString()}`;
    }

    if (event.type === "PULL_REQUEST") {
      text = `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${new Date(event.timestamp).toUTCString()}`;
    }

    if (event.type === "MERGE") {
      text = `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${new Date(event.timestamp).toUTCString()}`;
    }

    const li = document.createElement("li");
    li.innerText = text;
    list.appendChild(li);
  });
}

setInterval(fetchEvents, 15000);
fetchEvents();
