package Backend;

import Exceptions.ProductNotFoundException;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class DataManager {

    private static final String PRODUCTS_FILE = "data/products.csv";
    private static final String USERS_FILE = "data/users.csv";
    private static final String ORDERS_FILE = "data/order.csv";

    private static final List<Product> products = new ArrayList<>();
    private static final List<User> users = new ArrayList<>();
    private static final List<Order> orders = new ArrayList<>();

    static {
        loadProducts();
        loadUsers();
        loadOrders();
    }

    // --------------------------------------------------------
    //                     LOAD PRODUCTS
    // --------------------------------------------------------
    private static void loadProducts() {
        try (BufferedReader br = new BufferedReader(new FileReader(PRODUCTS_FILE))) {
            br.readLine();  // Skip header
            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 10) {
                    int sNo = Integer.parseInt(parts[0]);
                    String name = parts[1];
                    String id = parts[2];
                    double price = Double.parseDouble(parts[3]);
                    int quantity = Integer.parseInt(parts[4]);
                    String category = parts[5];
                    String brand = parts[6];
                    String desc = parts[7];
                    int rating = Integer.parseInt(parts[8]);
                    String image = parts[9];
                    products.add(new Product(sNo, name, id, price, quantity, category, brand, desc, rating, image));
                }
            }
        } catch (IOException e) {
            System.err.println("Error loading products: " + e.getMessage());
        }
    }

    // --------------------------------------------------------
    //                     LOAD USERS
    // --------------------------------------------------------
    private static void loadUsers() {
        try (BufferedReader br = new BufferedReader(new FileReader(USERS_FILE))) {
            br.readLine();  // Skip header
            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 6) {
                    String username = parts[1];
                    String password = parts[2];
                    String fullName = parts[3];
                    String email = parts[4];
                    Role role = Role.valueOf(parts[5].toUpperCase());

                    switch (role) {
                        case CUSTOMER -> users.add(new Customer(username, password, fullName, email));
                        case PREMIUM -> users.add(new PremiumUser(username, password, fullName, email));
                        case ADMIN -> users.add(new Admin(username, password, fullName, email));
                    }
                }
            }
        } catch (IOException e) {
            System.err.println("Error loading users: " + e.getMessage());
        }
    }

    // --------------------------------------------------------
    //                     LOAD ORDERS
    // --------------------------------------------------------
    private static void loadOrders() {
        try (BufferedReader br = new BufferedReader(new FileReader(ORDERS_FILE))) {
            br.readLine(); // Skip header
            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 5) {
                    int sNo = Integer.parseInt(parts[0]);
                    String username = parts[1];
                    String item = parts[2];
                    double cost = Double.parseDouble(parts[3]);
                    String time = parts[4];
                    orders.add(new Order(sNo, username, item, cost, time));
                }
            }
        } catch (IOException e) {
            System.err.println("Error loading orders: " + e.getMessage());
        }
    }

    // --------------------------------------------------------
    //                      PRODUCT METHODS
    // --------------------------------------------------------
    public static List<Product> getAllProducts() {
        return new ArrayList<>(products);
    }

    public static User getUser(String username, String password) {
        for (User user : users) {
            if (user.getUsername().equals(username) && user.password.equals(password)) {
                return user;
            }
        }
        return null;
    }

    public static void saveProducts() {
        try (PrintWriter pw = new PrintWriter(new FileWriter(PRODUCTS_FILE))) {
            pw.println("S.No,Product_Name,Product_ID,Price,Quantity,Category,Brand,Description,Rating(out_of_10),image");
            for (Product p : products) {
                pw.printf("%d,%s,%s,%.0f,%d,%s,%s,%s,%d,%s%n",
                        p.getSNo(), p.getName(), p.getId(), p.getPrice(), p.getQuantity(),
                        p.getCategory(), p.getBrand(), p.getDescription(), p.getRating(), p.getImagePath());
            }
        } catch (IOException e) {
            System.err.println("Error saving products: " + e.getMessage());
        }
    }

    public static void addProduct(Product product) {
        products.add(product);
        saveProducts();
    }

    public static void removeProduct(String productId) throws ProductNotFoundException {
        Product toRemove = null;
        for (Product p : products) {
            if (p.getId().equals(productId)) {
                toRemove = p;
                break;
            }
        }
        if (toRemove == null) {
            throw new ProductNotFoundException("Product not found: " + productId);
        }
        products.remove(toRemove);
        saveProducts();
    }

    public static void updateProductQuantity(String productId, int newQuantity) throws ProductNotFoundException {
        for (Product p : products) {
            if (p.getId().equals(productId)) {
                p.setQuantity(newQuantity);
                saveProducts();
                return;
            }
        }
        throw new ProductNotFoundException("Product not found: " + productId);
    }

    // --------------------------------------------------------
    //                      USER METHODS
    // --------------------------------------------------------
    public static void addUser(User user) {
        users.add(user);
        saveUsers();
    }

    private static void saveUsers() {
        try (PrintWriter pw = new PrintWriter(new FileWriter(USERS_FILE))) {
            pw.println("S.No,Username,Password,FullName,Email,Role");
            int sNo = 1;
            for (User u : users) {
                pw.printf("%d,%s,%s,%s,%s,%s%n",
                        sNo++, u.getUsername(), u.password, u.getFullName(), u.getEmail(), u.getRole().name());
            }
        } catch (IOException e) {
            System.err.println("Error saving users: " + e.getMessage());
        }
    }

    // --------------------------------------------------------
    //                      ORDER METHODS
    // --------------------------------------------------------
    public static List<Order> getUserOrders(String username) {
        List<Order> userOrders = new ArrayList<>();
        for (Order o : orders) {
            if (o.getUsername().equals(username)) {
                userOrders.add(o);
            }
        }
        return userOrders;
    }

    public static void addOrder(Order order) {
        orders.add(order);
        saveOrders();
    }

    private static void saveOrders() {
        try (PrintWriter pw = new PrintWriter(new FileWriter(ORDERS_FILE))) {
            pw.println("S.No,Username,Item,Cost,Time");
            for (Order o : orders) {
                pw.printf("%d,%s,%s,%.2f,%s%n",
                        o.getSNo(), o.getUsername(), o.getItem(), o.getCost(), o.getTime());
            }
        } catch (IOException e) {
            System.err.println("Error saving orders: " + e.getMessage());
        }
    }
}
