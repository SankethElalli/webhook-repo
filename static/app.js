async function fetchEvents() {
    const res = await fetch('/events');
    const events = await res.json();
    const list = document.getElementById('events');
    list.innerHTML = '';
    if (events.length === 0) {
        const empty = document.createElement('li');
        empty.className = 'empty-msg';
        empty.textContent = 'No events yet.';
        list.appendChild(empty);
        return;
    }
    events.forEach(ev => {
        const li = document.createElement('li');
        li.className = 'event-item';
        li.textContent = ev.display;
        list.appendChild(li);
    });
}
fetchEvents();
setInterval(fetchEvents, 15000);