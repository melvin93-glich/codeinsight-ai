package Backend;

public class Discount {

    private Discount() {}  // Private constructor

    public static double applyDiscount(double total, double percent) {
        return total * (1 - percent / 100);
    }
}