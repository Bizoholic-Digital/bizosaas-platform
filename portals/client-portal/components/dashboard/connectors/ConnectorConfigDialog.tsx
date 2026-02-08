import { useState } from 'react'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert" // Assuming Alert exists
import { Loader2 } from "lucide-react"
import { brainApi } from '@/lib/brain-api'
import type { Connector } from '@/lib/brain-api'

interface ConnectorConfigDialogProps {
    connector: Connector | null
    isOpen: boolean
    onClose: () => void
    onSuccess: (connectorId: string) => void
}

export function ConnectorConfigDialog({
    connector,
    isOpen,
    onClose,
    onSuccess
}: ConnectorConfigDialogProps) {
    const [formData, setFormData] = useState<Record<string, string>>({})
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    if (!connector) return null

    const authSchema = connector.auth_schema || {}
    const fields = Object.entries(authSchema as Record<string, any>)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError('')

        try {
            await brainApi.connectors.connect(connector.id, formData)
            onSuccess(connector.id)
            onClose()
        } catch (err: any) {
            setError(err.message || 'Failed to connect. Please check credentials.')
        } finally {
            setLoading(false)
        }
    }

    const handleInputChange = (field: string, value: string) => {
        setFormData(prev => ({ ...prev, [field]: value }))
    }

    return (
        <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <div className="flex items-center gap-3">
                        {/* If we had icon rendering logic, it would go here */}
                        <DialogTitle>Connect {connector.name}</DialogTitle>
                    </div>
                    <DialogDescription>
                        Enter your credentials to enable {connector.name} integration.
                    </DialogDescription>
                </DialogHeader>

                <form onSubmit={handleSubmit} className="space-y-4 py-4">
                    {error && (
                        <div className="p-3 text-sm text-red-500 bg-red-50 rounded-md">
                            {error}
                        </div>
                    )}

                    {fields.length === 0 ? (
                        <p className="text-sm text-muted-foreground">
                            No configuration required for this connector. Click Connect to proceed.
                        </p>
                    ) : (
                        fields.map(([key, field]: [string, any]) => (
                            <div key={key} className="space-y-2">
                                <Label htmlFor={key}>{field.label || key}</Label>
                                <Input
                                    id={key}
                                    type={field.type === 'password' || key.toLowerCase().includes('password') ? 'password' : 'text'}
                                    placeholder={field.placeholder}
                                    value={formData[key] || ''}
                                    onChange={(e) => handleInputChange(key, e.target.value)}
                                    disabled={loading}
                                    required={!field.optional}
                                />
                                {field.help && (
                                    <p className="text-xs text-muted-foreground">{field.help}</p>
                                )}
                            </div>
                        ))
                    )}

                    <DialogFooter>
                        <Button type="button" variant="outline" onClick={onClose} disabled={loading}>
                            Cancel
                        </Button>
                        <Button type="submit" disabled={loading}>
                            {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                            {loading ? 'Connecting...' : 'Connect'}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    )
}
