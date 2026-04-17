import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter Account Holder Name : ");
        String name = scanner.nextLine();

        System.out.print("Enter Initial Balance      : ₹");
        double initialBalance = scanner.nextDouble();

        Account account = new Account(name, initialBalance);

        System.out.println("\nAccount created for " + name);

        int choice = 0;

        while (choice != 4) {
            System.out.println("\n========= FinSafe Menu =========");
            System.out.println("1. Deposit");
            System.out.println("2. Withdraw / Spend");
            System.out.println("3. View Mini Statement");
            System.out.println("4. Exit");
            System.out.println("================================");
            System.out.print("Enter your choice: ");
            choice = scanner.nextInt();

            switch (choice) {

                case 1:
                    System.out.print("Enter deposit amount: ₹");
                    double depositAmount = scanner.nextDouble();
                    try {
                        account.deposit(depositAmount);
                    } catch (IllegalArgumentException e) {
                        System.out.println("Error: " + e.getMessage());
                    }
                    break;

                case 2:
                    System.out.print("Enter spend amount: ₹");
                    double spendAmount = scanner.nextDouble();
                    try {
                        account.processTransaction(spendAmount);
                    } catch (FundsException e) {
                        System.out.println("Error: " + e.getMessage());
                    } catch (IllegalArgumentException e) {
                        System.out.println("Error: " + e.getMessage());
                    }
                    break;

                case 3:
                    account.printMiniStatement();
                    break;

                case 4:
                    System.out.println("\nThank you for using FinSafe. Have a good day!");
                    break;

                default:
                    System.out.println("Invalid choice. Please enter 1-4.");
            }
        }

        scanner.close();
    }
}