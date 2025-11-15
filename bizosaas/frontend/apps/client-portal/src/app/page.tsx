import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export default async function Home() {
  // Check for auth token on server-side
  const cookieStore = await cookies()
  const hasToken = cookieStore.has('access_token')

  // Redirect based on authentication status
  if (hasToken) {
    redirect('/dashboard')
  } else {
    redirect('/login')
  }
}
