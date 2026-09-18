import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Northstar Ops | Vendor Intake Automation',
  description: 'Lightweight workflow automation for vendor requests, onboarding notes, and internal service coordination.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
