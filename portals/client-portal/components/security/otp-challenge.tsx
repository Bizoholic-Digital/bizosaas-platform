"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ShieldAlert, Timer, CheckCircle2 } from "lucide-react"

interface OTPChallengeProps {
    isOpen: boolean
    onClose: () => void
    onSuccess: () => void
    actionLabel: string
    actionSeverity: "critical" | "warning"
}

export function OTPChallenge({ isOpen, onClose, onSuccess, actionLabel, actionSeverity }: OTPChallengeProps) {
    const [step, setStep] = useState<"password" | "otp" | "success">("password")
    const [password, setPassword] = useState("")
    const [otp, setOtp] = useState("")
    const [timer, setTimer] = useState(60)
    const [isLoading, setIsLoading] = useState(false)

    useEffect(() => {
        let interval: any
        if (step === "otp" && timer > 0) {
            interval = setInterval(() => setTimer((t) => t - 1), 1000)
        }
        return () => clearInterval(interval)
    }, [step, timer])

    const handlePasswordSubmit = async () => {
        setIsLoading(true)
        // Simulated API call for password verification and OTP trigger
        setTimeout(() => {
            setIsLoading(false)
            setStep("otp")
            setTimer(60)
        }, 1000)
    }

    const handleOTPSubmit = async () => {
        setIsLoading(true)
        // Simulated API call for OTP verification
        setTimeout(() => {
            setIsLoading(false)
            setStep("success")
            setTimeout(() => {
                onSuccess()
                onClose()
                // Reset for next time
                setStep("password")
                setPassword("")
                setOtp("")
            }, 1500)
        }, 1000)
    }

    return (
        <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
            <DialogContent className="sm:max-w-[425px]">
                {step === "password" && (
                    <>
                        <DialogHeader>
                            <div className="flex items-center gap-2 mb-2">
                                <ShieldAlert className={actionSeverity === "critical" ? "text-destructive" : "text-yellow-500"} />
                                <DialogTitle>Critical Action Required</DialogTitle>
                            </div>
                            <DialogDescription>
                                Confirming: <strong>{actionLabel}</strong>. For your security, please re-authenticate with your password.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="grid gap-4 py-4">
                            <div className="grid gap-2">
                                <Label htmlFor="password">Password</Label>
                                <Input
                                    id="password"
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="Enter your password"
                                />
                            </div>
                        </div>
                        <DialogFooter>
                            <Button variant="outline" onClick={onClose}>Cancel</Button>
                            <Button onClick={handlePasswordSubmit} disabled={!password || isLoading}>
                                {isLoading ? "Verifying..." : "Next Step"}
                            </Button>
                        </DialogFooter>
                    </>
                )}

                {step === "otp" && (
                    <>
                        <DialogHeader>
                            <DialogTitle>Verification Code</DialogTitle>
                            <DialogDescription>
                                We've sent a 6-digit code to your registered email and mobile number.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="grid gap-4 py-4">
                            <div className="grid gap-2">
                                <Label htmlFor="otp">One-Time Password (OTP)</Label>
                                <Input
                                    id="otp"
                                    maxLength={6}
                                    value={otp}
                                    onChange={(e) => setOtp(e.target.value)}
                                    className="text-center text-2xl tracking-[0.5em] font-mono"
                                    placeholder="000000"
                                />
                                <div className="flex justify-between items-center mt-2 text-sm">
                                    <span className="flex items-center text-muted-foreground">
                                        <Timer className="mr-1 h-3 w-3" />
                                        Expires in {timer}s
                                    </span>
                                    <Button variant="link" className="h-auto p-0" disabled={timer > 0}>
                                        Resend Code
                                    </Button>
                                </div>
                            </div>
                        </div>
                        <DialogFooter>
                            <Button variant="outline" onClick={() => setStep("password")}>Back</Button>
                            <Button onClick={handleOTPSubmit} disabled={otp.length < 6 || isLoading}>
                                {isLoading ? "Verifying..." : "Confirm Action"}
                            </Button>
                        </DialogFooter>
                    </>
                )}

                {step === "success" && (
                    <div className="py-10 flex flex-col items-center justify-center text-center gap-4">
                        <CheckCircle2 className="h-16 w-16 text-green-500 animate-in zoom-in duration-300" />
                        <div>
                            <DialogTitle>Verified Successfully</DialogTitle>
                            <DialogDescription className="mt-2">
                                The critical change has been authenticated and processed.
                            </DialogDescription>
                        </div>
                    </div>
                )}
            </DialogContent>
        </Dialog>
    )
}
