package Backend;

public class Customer extends User {
    private final ShoppingCart cart;

    public Customer(String username, String password, String fullName, String email) {
        super(username, password, fullName, email, Role.CUSTOMER);
        this.cart = new ShoppingCart();
    }

    public ShoppingCart getCart() {
        return cart;
    }

    @Override
    public void performAction() {
        // Customer actions like browsing, adding to cart
    }

    public double calculateTotal() {
        return cart.calculateTotal();
    }
}