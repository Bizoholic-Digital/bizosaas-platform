import { redirect } from 'next/navigation'

export default function LoginPage() {
  // Redirect to portal login
  redirect('/portal/login')
}