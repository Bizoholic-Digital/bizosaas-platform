"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ShieldCheck, Fingerprint, Smartphone, CheckCircle2, AlertCircle } from "lucide-react"

interface MFAChallengeProps {
    isOpen: boolean
    onClose: () => void
    onSuccess: () => void
    actionLabel: string
    actionSeverity: "critical" | "warning"
}

export function MFAChallenge({ isOpen, onClose, onSuccess, actionLabel, actionSeverity }: MFAChallengeProps) {
    const [method, setMethod] = useState<"totp" | "passkey">("totp")
    const [step, setStep] = useState<"challenge" | "success">("challenge")
    const [otp, setOtp] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const handleTOTPSubmit = async (e?: React.FormEvent) => {
        e?.preventDefault()
        setIsLoading(true)
        setError(null)

        // Simulated TOTP/2FAS verification
        setTimeout(() => {
            if (otp === "123456") { // Simulation logic
                setIsLoading(false)
                setStep("success")
                finishChallenge()
            } else {
                setIsLoading(false)
                setError("Invalid verification code. Please try again.")
            }
        }, 1000)
    }

    const handlePasskeySubmit = async () => {
        setIsLoading(true)
        setError(null)

        // Simulated WebAuthn / Passkey logic
        try {
            // In a real app: await navigator.credentials.get(...)
            setTimeout(() => {
                setIsLoading(false)
                setStep("success")
                finishChallenge()
            }, 1500)
        } catch (err) {
            setIsLoading(false)
            setError("Passkey authentication failed.")
        }
    }

    const finishChallenge = () => {
        setTimeout(() => {
            onSuccess()
            onClose()
            // Reset
            setStep("challenge")
            setOtp("")
        }, 1500)
    }

    return (
        <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
            <DialogContent className="sm:max-w-[450px]">
                {step === "challenge" && (
                    <>
                        <DialogHeader>
                            <div className="flex items-center gap-2 mb-2">
                                <ShieldCheck className={actionSeverity === "critical" ? "text-destructive" : "text-blue-500"} />
                                <DialogTitle>Security Verification Required</DialogTitle>
                            </div>
                            <DialogDescription>
                                Confirming: <strong>{actionLabel}</strong>. Please use your secondary factor to authorize this sensitive action.
                            </DialogDescription>
                        </DialogHeader>

                        <Tabs defaultValue="totp" className="w-full mt-4" onValueChange={(v) => setMethod(v as any)}>
                            <TabsList className="grid w-full grid-cols-2">
                                <TabsTrigger value="totp" className="flex items-center gap-2">
                                    <Smartphone className="h-4 w-4" /> Authenticator
                                </TabsTrigger>
                                <TabsTrigger value="passkey" className="flex items-center gap-2">
                                    <Fingerprint className="h-4 w-4" /> Passkey
                                </TabsTrigger>
                            </TabsList>

                            <TabsContent value="totp" className="py-6 space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="otp">Code from Authenticator App (2FAS/Google)</Label>
                                    <Input
                                        id="otp"
                                        maxLength={6}
                                        value={otp}
                                        onChange={(e) => setOtp(e.target.value)}
                                        className="text-center text-3xl tracking-[0.6em] font-mono h-14"
                                        placeholder="000000"
                                        autoFocus
                                    />
                                    {error && <p className="text-xs text-destructive flex items-center gap-1"><AlertCircle className="h-3 w-3" /> {error}</p>}
                                </div>
                                <Button className="w-full h-12 text-lg" onClick={() => handleTOTPSubmit()} disabled={otp.length < 6 || isLoading}>
                                    {isLoading ? "Verifying..." : "Confirm with TOTP"}
                                </Button>
                            </TabsContent>

                            <TabsContent value="passkey" className="py-8 text-center space-y-6">
                                <div className="flex justify-center">
                                    <div className="p-4 bg-muted rounded-full">
                                        <Fingerprint className="h-12 w-12 text-blue-600" />
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    <h3 className="font-semibold">Use Managed Passkey</h3>
                                    <p className="text-sm text-muted-foreground px-8"> Use your fingerprint, face, or screen lock to securely authorize this request. </p>
                                </div>
                                <Button className="w-full h-12 text-lg" onClick={handlePasskeySubmit} disabled={isLoading}>
                                    {isLoading ? "Authenticating..." : "Authorize with Passkey"}
                                </Button>
                            </TabsContent>
                        </Tabs>

                        <DialogFooter className="sm:justify-start">
                            <Button variant="ghost" className="text-muted-foreground text-xs" onClick={onClose}>
                                Cancel and abort action
                            </Button>
                        </DialogFooter>
                    </>
                )}

                {step === "success" && (
                    <div className="py-12 flex flex-col items-center justify-center text-center gap-6">
                        <div className="bg-green-100 p-4 rounded-full">
                            <CheckCircle2 className="h-16 w-16 text-green-600 animate-in zoom-in duration-500" />
                        </div>
                        <div>
                            <DialogTitle className="text-2xl">Identity Verified</DialogTitle>
                            <DialogDescription className="mt-2 text-base">
                                Critical authorization granted. Processing your request now...
                            </DialogDescription>
                        </div>
                    </div>
                )}
            </DialogContent>
        </Dialog>
    )
}
