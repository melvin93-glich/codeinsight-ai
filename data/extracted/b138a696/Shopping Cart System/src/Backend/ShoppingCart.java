package Backend;

import Exceptions.OutOfStockException;

import java.util.ArrayList;
import java.util.List;

public class ShoppingCart {
    private final List<Product> items = new ArrayList<>();
    private static final int MAX_ITEMS = 8;

    public void addProduct(Product product) throws OutOfStockException {
        if (product.getQuantity() <= 0) {
            throw new OutOfStockException("Product " + product.getName() + " is out of stock.");
        }
        if (items.size() >= MAX_ITEMS) {
            throw new IllegalStateException("Cart cannot hold more than " + MAX_ITEMS + " items.");
        }
        items.add(product);
        product.setQuantity(product.getQuantity() - 1);  // Deduct stock
    }

    public void removeProduct(Product product) {
        items.remove(product);
        product.setQuantity(product.getQuantity() + 1);  // Restore stock
    }

    public List<Product> getItems() {
        return new ArrayList<>(items);  // Defensive copy
    }

    public double calculateTotal() {
        double total = 0;
        for (Product p : items) {
            total += p.getPrice();
        }
        return total;
    }

    public void clear() {
        items.clear();
    }
}