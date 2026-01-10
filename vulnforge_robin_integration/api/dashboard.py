from __future__ import annotations


DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>VulnForge Robin Review</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 2rem; background: #0f172a; color: #e2e8f0; }
      a { color: #60a5fa; }
      table { border-collapse: collapse; width: 100%; margin-top: 1rem; }
      th, td { border: 1px solid #1e293b; padding: 0.5rem; text-align: left; }
      th { background: #1e293b; }
      tr:nth-child(even) { background: #111827; }
      .score { font-weight: bold; }
      .actions button { margin-right: 0.5rem; }
      #details { white-space: pre-wrap; background: #111827; padding: 1rem; margin-top: 1rem; border-radius: 0.5rem; }
    </style>
  </head>
  <body>
    <h1>VulnForge Robin Integration</h1>
    <p>Review latest dark web OSINT items. All ingestion happens offline; this UI only reads normalized data.</p>
    <section>
      <label for="filterType">Leak Type:</label>
      <input id="filterType" type="text" placeholder="credentials" />
      <label for="minScore">Min Score:</label>
      <input id="minScore" type="number" min="0" max="100" />
      <button onclick="loadItems()">Refresh</button>
    </section>
    <table id="itemsTable">
      <thead>
        <tr>
          <th>ID</th>
          <th>Target</th>
          <th>Leak Type</th>
          <th>Source</th>
          <th>Score</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
    <div id="details"></div>
    <script>
      async function loadItems() {
        const type = document.getElementById('filterType').value;
        const minScore = document.getElementById('minScore').value;
        const params = new URLSearchParams();
        if (type) params.append('leak_type', type);
        if (minScore) params.append('min_score', minScore);
        const resp = await fetch('/items?' + params.toString());
        const data = await resp.json();
        const tbody = document.querySelector('#itemsTable tbody');
        tbody.innerHTML = '';
        data.items.forEach(item => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${item.id}</td>
            <td>${item.target.value}</td>
            <td>${item.leak_type}</td>
            <td>${item.source}</td>
            <td class="score">${item.score}</td>
            <td class="actions">
              <button onclick="viewItem('${item.id}')">View</button>
              <button onclick="recordAction('${item.id}', 'approve')">Approve</button>
              <button onclick="recordAction('${item.id}', 'archive')">Archive</button>
            </td>
          `;
          tbody.appendChild(tr);
        });
      }

      async function viewItem(id) {
        const resp = await fetch('/items/' + id);
        const data = await resp.json();
        document.getElementById('details').textContent = JSON.stringify(data, null, 2);
      }

      async function recordAction(id, action) {
        const actor = prompt('Enter your name for audit log:');
        if (!actor) return;
        const body = { action, actor };
        await fetch('/items/' + id + '/actions', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body)
        });
        alert('Action recorded');
        loadItems();
      }

      loadItems();
    </script>
  </body>
</html>
"""


def render_dashboard() -> str:
    return DASHBOARD_HTML
