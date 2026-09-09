package Backend;

import java.util.Random;


public class PremiumUser extends Customer {

    // Reuse a single Random instance to avoid Sonar warning about repeated creation.
    private static final Random RNG = new Random();

    public PremiumUser(String username, String password, String fullName, String email) {
        super(username, password, fullName, email);
        this.role = Role.PREMIUM;
    }

    @Override
    public double calculateTotal() {
        double total = super.calculateTotal();
        // discount between 20 and 50 percent
        double discountPercent = 20.0 + RNG.nextDouble() * 30.0;
        double discounted = total * (1.0 - discountPercent / 100.0);
        return discounted;
    }
}
