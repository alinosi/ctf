'use server'

type DemoRequest = {
  name: string
  workEmail: string
  company: string
  notes: string
}

export async function processData(data: DemoRequest): Promise<string> {
  await new Promise(resolve => setTimeout(resolve, 100))
  return `Thanks ${data.name}. We will reach out at ${data.workEmail} after reviewing ${data.company} and your intake notes.`
}
