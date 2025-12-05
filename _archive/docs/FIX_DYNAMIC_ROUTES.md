# Fix for Dynamic Route TypeScript Errors

## Issue
Next.js 15 with client components using dynamic routes has TypeScript errors.

## Affected Files
1. `/app/(auth)/reset-password/[token]/page.tsx`
2. `/app/(auth)/verify-email/[token]/page.tsx`
3. `/app/blog/[slug]/page.tsx`
4. `/app/case-studies/[slug]/page.tsx`
5. `/app/dashboard/campaigns/[id]/page.tsx`

## Solution
For client components with dynamic routes in Next.js 15, use `useParams()` hook instead of params prop:

```typescript
// WRONG (causes error):
export default function Page({ params }: { params: { token: string } }) {
  const token = params.token
  ...
}

// CORRECT:
'use client'
import { useParams } from 'next/navigation'

export default function Page() {
  const params = useParams()
  const token = params.token as string
  ...
}
```

## Quick Fix Commands

Run this from service directory:

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas/misc/services/bizoholic-frontend

# Fix reset-password
sed -i 's/export default function ResetPasswordPage({ params }: { params: { token: string } })/export default function ResetPasswordPage()/' src/app/\(auth\)/reset-password/\[token\]/page.tsx
sed -i '8a import { useParams } from '"'"'next/navigation'"'"'' src/app/\(auth\)/reset-password/\[token\]/page.tsx
sed -i '11a  const params = useParams()' src/app/\(auth\)/reset-password/\[token\]/page.tsx
sed -i '12a  const token = params.token as string' src/app/\(auth\)/reset-password/\[token\]/page.tsx

# Repeat for other dynamic routes...
```

## Alternative: Use Agent to Fix

Use the general-purpose agent to systematically fix all 5 dynamic route files.
