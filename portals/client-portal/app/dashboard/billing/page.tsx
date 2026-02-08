"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { CreditCard, Download, Plus, RefreshCw, AlertCircle } from "lucide-react"
import { useToast } from "@/components/ui/use-toast"
import { OTPChallenge } from "@/components/security/otp-challenge"

interface Transaction {
    id: string
    date: string
    amount: number
    description: string
    status: "completed" | "pending" | "failed"
    invoice_url?: string
}

export default function BillingPage() {
    const { toast } = useToast()
    const [balance, setBalance] = useState(0)
    const [isLoading, setIsLoading] = useState(true)
    const [transactions, setTransactions] = useState<Transaction[]>([])
    const [isOTPChallengeOpen, setIsOTPChallengeOpen] = useState(false)

    useEffect(() => {
        // Simulate fetching data
        const fetchData = async () => {
            setIsLoading(true)
            // TODO: Replace with actual API call to /api/brain/billing/wallet
            setTimeout(() => {
                setBalance(150.00) // Mock balance
                setTransactions([
                    { id: "tx_1", date: "2026-02-01", amount: 50.00, description: "Wallet Top-up", status: "completed" },
                    { id: "tx_2", date: "2026-01-28", amount: -25.00, description: "SEO Audit Service", status: "completed" },
                    { id: "tx_3", date: "2026-01-15", amount: 100.00, description: "Initial Deposit", status: "completed" },
                ])
                setIsLoading(false)
            }, 1000)
        }
        fetchData()
    }, [])

    const handleTopUp = () => {
        setIsOTPChallengeOpen(true)
    }

    const onOTPSuccess = () => {
        toast({
            title: "Redirecting to Payment",
            description: "Initiating secure checkout session...",
        })
    }

    return (
        <div className="container mx-auto py-10 space-y-8">
            <OTPChallenge
                isOpen={isOTPChallengeOpen}
                onClose={() => setIsOTPChallengeOpen(false)}
                onSuccess={onOTPSuccess}
                actionLabel="Wallet Top-up"
                actionSeverity="warning"
            />
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Billing & Wallet</h2>
                    <p className="text-muted-foreground">Manage your prepaid balance and view transaction history.</p>
                </div>
                <Button onClick={handleTopUp}>
                    <Plus className="mr-2 h-4 w-4" /> Add Funds
                </Button>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Current Balance</CardTitle>
                        <CreditCard className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">${balance.toFixed(2)}</div>
                        <p className="text-xs text-muted-foreground">
                            +10% bonus on top-ups over $500
                        </p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Monthly Usage</CardTitle>
                        <RefreshCw className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">$25.00</div>
                        <Progress value={25} className="mt-2" />
                        <p className="text-xs text-muted-foreground mt-2">
                            15% of projected monthly budget
                        </p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Auto-Recharge</CardTitle>
                        <AlertCircle className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">In-Active</div>
                        <p className="text-xs text-muted-foreground">
                            Enable to avoid service interruption
                        </p>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Transaction History</CardTitle>
                    <CardDescription>Recent wallet activity and invoices.</CardDescription>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Date</TableHead>
                                <TableHead>Description</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Amount</TableHead>
                                <TableHead className="text-right">Invoice</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {transactions.map((tx) => (
                                <TableRow key={tx.id}>
                                    <TableCell>{tx.date}</TableCell>
                                    <TableCell>{tx.description}</TableCell>
                                    <TableCell>
                                        <Badge variant={tx.status === "completed" ? "default" : "destructive"}>
                                            {tx.status}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className={`text-right ${tx.amount > 0 ? "text-green-600" : ""}`}>
                                        {tx.amount > 0 ? "+" : ""}{tx.amount.toFixed(2)}
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="ghost" size="icon">
                                            <Download className="h-4 w-4" />
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    )
}
