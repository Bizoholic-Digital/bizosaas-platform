'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/lib/auth'

interface TagConfig {
    id: string
    container_id: string
    label: string
    environment: string
    is_active: boolean
}

export default function TagsPage() {
    const { user, getToken } = useAuth()
    const [tags, setTags] = useState<TagConfig[]>([])
    const [loading, setLoading] = useState(true)
    const [saving, setSaving] = useState(false)
    const [containerId, setContainerId] = useState('')
    const [message, setMessage] = useState('')

    useEffect(() => {
        if (user) {
            fetchTags()
        }
    }, [user])

    const fetchTags = async () => {
        try {
            const token = await getToken()
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/tags/gtm`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            if (res.ok) {
                const data = await res.json()
                setTags(data)
                // Pre-fill if exists
                if (data.length > 0) {
                    setContainerId(data[0].container_id)
                }
            }
        } catch (error) {
            console.error('Failed to fetch tags', error)
        } finally {
            setLoading(false)
        }
    }

    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault()
        setSaving(true)
        setMessage('')

        try {
            const token = await getToken()
            const method = tags.length > 0 ? 'PUT' : 'POST'
            const url = tags.length > 0
                ? `${process.env.NEXT_PUBLIC_API_URL}/tags/gtm/${tags[0].id}`
                : `${process.env.NEXT_PUBLIC_API_URL}/tags/gtm`

            const res = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    container_id: containerId,
                    label: 'Main Website',
                    environment: 'production'
                })
            })

            if (res.ok) {
                setMessage('GTM Container ID saved successfully!')
                fetchTags()
            } else {
                const error = await res.json()
                setMessage(`Error: ${error.detail || 'Failed to save'}`)
            }
        } catch (error) {
            setMessage('An error occurred. Please try again.')
        } finally {
            setSaving(false)
        }
    }

    if (loading) return <div className="p-8">Loading settings...</div>

    return (
        <div className="max-w-4xl mx-auto py-8 px-4">
            <h1 className="text-2xl font-bold mb-6">Google Tag Manager Integration</h1>

            <div className="bg-white rounded-lg shadow p-6 mb-8">
                <h2 className="text-xl font-semibold mb-4">Container Configuration</h2>
                <p className="text-gray-600 mb-6">
                    Connect your Google Tag Manager container to enable analytics, marketing pixels, and tracking on your website.
                </p>

                <form onSubmit={handleSave} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            GTM Container ID
                        </label>
                        <input
                            type="text"
                            value={containerId}
                            onChange={(e) => setContainerId(e.target.value)}
                            placeholder="GTM-XXXXXXX"
                            className="w-full max-w-md px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            required
                        />
                        <p className="text-sm text-gray-500 mt-1">
                            Found in your GTM Workspace header (starts with GTM-)
                        </p>
                    </div>

                    <div className="flex items-center gap-4">
                        <button
                            type="submit"
                            disabled={saving}
                            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
                        >
                            {saving ? 'Saving...' : 'Save Configuration'}
                        </button>
                        {message && (
                            <span className={`text-sm ${message.includes('Error') ? 'text-red-600' : 'text-green-600'}`}>
                                {message}
                            </span>
                        )}
                    </div>
                </form>
            </div>

            {tags.length > 0 && (
                <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-xl font-semibold mb-4">Installation Instructions</h2>
                    <p className="mb-4 text-gray-600">
                        For custom websites, copy and paste these snippets into your site code.
                        <br />
                        <strong>Note:</strong> If you use our Managed Website service, this is handled automatically.
                    </p>

                    <div className="space-y-6">
                        <div>
                            <h3 className="font-medium mb-2">1. Paste this in the <code>&lt;head&gt;</code> of the page:</h3>
                            <div className="bg-gray-50 p-4 rounded-md border text-xs font-mono overflow-x-auto">
                                {`<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','${tags[0].container_id}');</script>
<!-- End Google Tag Manager -->`}
                            </div>
                        </div>

                        <div>
                            <h3 className="font-medium mb-2">2. Paste this immediately after the opening <code>&lt;body&gt;</code> tag:</h3>
                            <div className="bg-gray-50 p-4 rounded-md border text-xs font-mono overflow-x-auto">
                                {`<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=${tags[0].container_id}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->`}
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
