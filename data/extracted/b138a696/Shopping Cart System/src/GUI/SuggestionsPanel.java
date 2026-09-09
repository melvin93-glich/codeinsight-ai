package GUI;

import Backend.*;
import Exceptions.OutOfStockException;

import javax.swing.*;
import java.awt.*;
import java.util.List;

public class SuggestionsPanel extends JPanel {
    public SuggestionsPanel(User user) {
        setLayout(new BorderLayout(10, 10));
        setBackground(UIConstants.BG_LIGHT);
        setBorder(BorderFactory.createEmptyBorder(12, 12, 12, 12));

        JLabel title = new JLabel("Recommended for you", SwingConstants.LEFT);
        title.setFont(UIConstants.H2);
        add(title, BorderLayout.NORTH);

        JPanel cards = new JPanel(new WrapLayout(FlowLayout.LEFT, 16, 16));
        cards.setBackground(UIConstants.BG_LIGHT);

        List<Product> suggestions;
        try {
            suggestions = Suggestions.getHighRatedSuggestions();
        } catch (Exception ex) {
            suggestions = List.of();
        }

        if (suggestions.isEmpty()) {
            JLabel empty = new JLabel("No recommendations yet", SwingConstants.CENTER);
            empty.setFont(UIConstants.REGULAR);
            cards.add(empty);
        } else {
            for (Product p : suggestions) {
                ProductCard card = new ProductCard(p, user instanceof Customer, e -> {
                    if (user instanceof Customer customer) {
                        try {
                            customer.getCart().addProduct(p);
                        } catch (OutOfStockException ex) {
                        }
                        DataManager.saveProducts();
                        JOptionPane.showMessageDialog(this, "Added to cart");
                    }
                });
                cards.add(card);
            }
        }

        add(new JScrollPane(cards), BorderLayout.CENTER);
    }
}
