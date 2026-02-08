"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { DollarSign, Users, CreditCard, ExternalLink, ArrowUpRight } from "lucide-react"

interface Transaction {
    id: string
    tenant: string
    date: string
    amount: number
    description: string
    status: "completed" | "pending" | "failed"
}

export default function AdminBillingPage() {
    const [revenue, setRevenue] = useState(0)
    const [transactions, setTransactions] = useState<Transaction[]>([])

    useEffect(() => {
        // Mock Data for Admin View
        setTimeout(() => {
            setRevenue(1250.00)
            setTransactions([
                { id: "tx_101", tenant: "Thrillring Gaming", date: "2026-02-01", amount: 500.00, description: "Wallet Top-up", status: "completed" },
                { id: "tx_102", tenant: "Coreldove Wellness", date: "2026-02-02", amount: 500.00, description: "Wallet Top-up", status: "completed" },
                { id: "tx_103", tenant: "Bizoholic Agency", date: "2026-01-25", amount: 250.00, description: "Monthly Subscription", status: "completed" },
            ])
        }, 500)
    }, [])

    return (
        <div className="container mx-auto py-10 space-y-8">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Billing & Revenue</h2>
                    <p className="text-muted-foreground">Overview of platform revenue and tenant billing status.</p>
                </div>
                <Button variant="outline" onClick={() => window.open('https://billing.bizoholic.net', '_blank')}>
                    <ExternalLink className="mr-2 h-4 w-4" /> Open Lago Dashboard
                </Button>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
                        <DollarSign className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">${revenue.toFixed(2)}</div>
                        <p className="text-xs text-muted-foreground">
                            +20.1% from last month
                        </p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Active Subscriptions</CardTitle>
                        <Users className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">3</div>
                        <p className="text-xs text-muted-foreground">
                            Across 3 tenants
                        </p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Stripe Balance</CardTitle>
                        <CreditCard className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">$1,215.50</div>
                        <p className="text-xs text-muted-foreground">
                            Available for payout
                        </p>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Recent Transactions</CardTitle>
                    <CardDescription>Latest payments across all tenants.</CardDescription>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Date</TableHead>
                                <TableHead>Tenant</TableHead>
                                <TableHead>Description</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Amount</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {transactions.map((tx) => (
                                <TableRow key={tx.id}>
                                    <TableCell>{tx.date}</TableCell>
                                    <TableCell className="font-medium">{tx.tenant}</TableCell>
                                    <TableCell>{tx.description}</TableCell>
                                    <TableCell>
                                        <Badge variant={tx.status === "completed" ? "default" : "secondary"}>
                                            {tx.status}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        ${tx.amount.toFixed(2)}
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
