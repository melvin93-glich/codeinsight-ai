package Backend;

import java.util.List;

public class Suggestions {

    private Suggestions() {}  // Private constructor

    public static List<Product> getHighRatedSuggestions() {
        return DataManager.getAllProducts().stream()
                .filter(p -> p.getRating() >= 8)
                .limit(5)
                .toList();
    }
}