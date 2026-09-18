export async function ServerComponent() {
  const serverData = await fetchServerData()

  return (
    <aside className="status-panel">
      <div className="status-header">
        <span className="status-dot" aria-hidden="true" />
        <span>Live workspace snapshot</span>
      </div>
      <div className="status-metric">
        <strong>27</strong>
        <span>active intake requests this week</span>
      </div>
      <ul className="status-list">
        <li>Average first response: 2.4 hours</li>
        <li>Teams routed today: Procurement, IT, Finance</li>
        <li>Workspace status: {serverData}</li>
      </ul>
    </aside>
  )
}

async function fetchServerData() {
  return 'healthy'
}
