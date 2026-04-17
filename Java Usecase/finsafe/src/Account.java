import java.util.ArrayList;

public class Account {
    private String accountHolder;
    private double balance;
    private ArrayList<String> transactionHistory;

    public Account(String accountHolder, double initialBalance) {
        this.accountHolder = accountHolder;
        this.balance = initialBalance;
        this.transactionHistory = new ArrayList<>();
    }

    public String getAccountHolder() {
        return accountHolder;
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Deposit amount must be positive.");
        }
        balance += amount;
        addToHistory("Deposited: ₹" + amount);
        System.out.println("Successfully deposited ₹" + amount);
    }

    public void processTransaction(double amount) throws FundsException {
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive.");
        }
        if (amount > balance) {
            throw new FundsException(
                    "Insufficient funds! Available balance: ₹" + balance
            );
        }
        balance -= amount;
        addToHistory("Spent: ₹" + amount);
        System.out.println("Transaction successful! Remaining balance: ₹" + balance);
    }

    private void addToHistory(String record) {
        if (transactionHistory.size() >= 5) {
            transactionHistory.remove(0);
        }
        transactionHistory.add(record);
    }

    public void printMiniStatement() {
        System.out.println("\n========= Mini Statement =========");
        System.out.println("Account Holder : " + accountHolder);
        System.out.println("Current Balance: ₹" + balance);
        System.out.println("Last " + transactionHistory.size() + " Transactions:");
        if (transactionHistory.isEmpty()) {
            System.out.println("  No transactions yet.");
        } else {
            for (int i = 0; i < transactionHistory.size(); i++) {
                System.out.println("  " + (i + 1) + ". " + transactionHistory.get(i));
            }
        }
        System.out.println("==================================\n");
    }
}
