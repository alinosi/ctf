'use client'

import { useState } from 'react'
import { processData } from '../actions/serverActions'

export function ServerActionForm() {
  const [formData, setFormData] = useState({
    name: '',
    workEmail: '',
    company: '',
    notes: '',
  })
  const [result, setResult] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setResult(null)
    setError(null)

    try {
      const response = await processData(formData)
      setResult(response)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    }
  }

  return (
    <div className="form-card">
      <form onSubmit={handleSubmit} className="lead-form">
        <div className="form-group">
          <label htmlFor="name">Full name</label>
          <input
            id="name"
            type="text"
            value={formData.name}
            onChange={(e) => setFormData((current) => ({ ...current, name: e.target.value }))}
            placeholder="Jordan Lee"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="workEmail">Work email</label>
          <input
            id="workEmail"
            type="email"
            value={formData.workEmail}
            onChange={(e) => setFormData((current) => ({ ...current, workEmail: e.target.value }))}
            placeholder="jordan@company.com"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="company">Company</label>
          <input
            id="company"
            type="text"
            value={formData.company}
            onChange={(e) => setFormData((current) => ({ ...current, company: e.target.value }))}
            placeholder="Northwind Freight"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="notes">What are you trying to improve?</label>
          <textarea
            id="notes"
            value={formData.notes}
            onChange={(e) => setFormData((current) => ({ ...current, notes: e.target.value }))}
            placeholder="We want a cleaner process for vendor onboarding, approvals, and internal follow-ups."
            rows={5}
            required
          />
        </div>
        <button type="submit">Request demo</button>
      </form>

      {result && (
        <div className="result">
          <h3>Request received</h3>
          <p>{result}</p>
        </div>
      )}

      {error && (
        <div className="result error">
          <h3>Submission error</h3>
          <p>{error}</p>
        </div>
      )}
    </div>
  )
}
