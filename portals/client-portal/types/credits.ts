export interface CreditsBalance {
    totalCredits: number;
    usedCredits: number;
    availableCredits: number;
    lastUpdated: string;
}

export interface CreditTransaction {
    id: string;
    type: 'earned' | 'spent' | 'purchased' | 'refunded';
    amount: number;
    description: string;
    date: string;
    status: 'completed' | 'pending' | 'failed';
}

export interface CreditsData {
    balance: CreditsBalance;
    transactions: CreditTransaction[];
}
