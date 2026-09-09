package Backend;

import java.util.ArrayList;
import java.util.List;

public class SearchProducts {

    private SearchProducts() {}  // Private constructor for utility class

    /**
     * Search products by a general keyword — matches name, category, brand, or description.
     */
    public static List<Product> search(String keyword) {
        List<Product> results = new ArrayList<>();
        if (keyword == null || keyword.trim().isEmpty()) return results;

        String key = keyword.toLowerCase();
        for (Product p : DataManager.getAllProducts()) {
            if (matches(p, key)) {
                results.add(p);
            }
        }
        return results;
    }

    /**
     * Helper method — checks if a product matches the search keyword.
     */
    private static boolean matches(Product p, String key) {
        return (p.getName() != null && p.getName().toLowerCase().contains(key))
            || (p.getCategory() != null && p.getCategory().toLowerCase().contains(key))
            || (p.getBrand() != null && p.getBrand().toLowerCase().contains(key))
            || (p.getDescription() != null && p.getDescription().toLowerCase().contains(key));
    }

    /**
     * For compatibility — still supports explicit name search.
     */
    public static List<Product> searchByName(String name) {
        return search(name);
    }

    /**
     * For compatibility — still supports explicit category search.
     */
    public static List<Product> searchByCategory(String category) {
        return search(category);
    }
}
