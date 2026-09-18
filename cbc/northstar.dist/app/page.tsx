import { ServerActionForm } from './components/ServerActionForm'
import { ServerComponent } from './components/ServerComponent'

export default function Home() {
  return (
    <main className="page-shell">
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">Northstar Ops</span>
          <h1>Vendor intake that does not get buried in inboxes.</h1>
          <p className="hero-text">
            Centralize supplier requests, route approvals faster, and keep shared
            context in one place for procurement, IT, and operations.
          </p>
          <div className="hero-actions">
            <a className="primary-link" href="#request-demo">Request a demo</a>
            <a className="secondary-link" href="#platform-overview">See platform overview</a>
          </div>
        </div>
        <ServerComponent />
      </section>

      <section className="info-grid" id="platform-overview">
        <article className="info-card">
          <h2>Shared intake queue</h2>
          <p>
            Replace ad-hoc forms and scattered email threads with one intake stream
            that procurement and IT can both triage.
          </p>
        </article>
        <article className="info-card">
          <h2>Faster approvals</h2>
          <p>
            Standardize request notes, attach vendor context early, and reduce the
            back-and-forth that slows down onboarding.
          </p>
        </article>
        <article className="info-card">
          <h2>Operational visibility</h2>
          <p>
            Give stakeholders a simple snapshot of open requests, environment
            health, and recent handoffs without another dashboard project.
          </p>
        </article>
      </section>

      <section className="quote-card">
        <p>
          "We used to lose basic vendor follow-ups in shared inboxes. Northstar gave
          our ops team a cleaner handoff process in a week."
        </p>
        <span>Operations Lead, regional logistics company</span>
      </section>

      <section className="cta-panel" id="request-demo">
        <div className="cta-copy">
          <span className="section-kicker">Request a walkthrough</span>
          <h2>Tell us how your team handles intake today.</h2>
          <p>
            We will tailor the demo around your approval flow, current tooling, and
            the handoffs that create the most friction.
          </p>
        </div>
        <ServerActionForm />
      </section>
    </main>
  )
}
