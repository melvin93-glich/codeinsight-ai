package Backend;

import java.io.Serializable;

public class Product implements Serializable {
    private final int sNo;
    private final String name;
    private final String id;
    private double price;
    private int quantity;
    private final String category;
    private final String brand;
    private final String description;
    private final int rating;
    private final String imagePath;

    public Product(int sNo, String name, String id, double price, int quantity, String category, String brand, String description, int rating, String imagePath) {
        this.sNo = sNo;
        this.name = name;
        this.id = id;
        this.price = price;
        this.quantity = quantity;
        this.category = category;
        this.brand = brand;
        this.description = description;
        this.rating = rating;
        this.imagePath = imagePath;
    }

    // Getters and setters
    public int getSNo() { return sNo; }
    public String getName() { return name; }
    public String getId() { return id; }
    public double getPrice() { return price; }
    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; }
    public String getCategory() { return category; }
    public String getBrand() { return brand; }
    public String getDescription() { return description; }
    public int getRating() { return rating; }
    public String getImagePath() { return imagePath; }

    @Override
    public String toString() {
        return name + " (" + id + ") - $" + price;
    }
}