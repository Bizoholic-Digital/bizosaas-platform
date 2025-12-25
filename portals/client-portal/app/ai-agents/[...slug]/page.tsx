import { redirect } from 'next/navigation';

interface Props {
    params: { slug: string[] };
}

export default function RedirectSlugPage({ params }: Props) {
    const path = params.slug?.join('/') || '';
    redirect(`/dashboard/ai-agents/${path}`);
}
