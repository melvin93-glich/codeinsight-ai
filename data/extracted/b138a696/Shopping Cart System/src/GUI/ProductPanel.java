package GUI;

import Backend.*;
import Exceptions.OutOfStockException;

import javax.swing.*;
import java.awt.*;
import java.util.List;

public class ProductPanel extends JPanel {
    private final User user;
    private final JPanel gridPanel;

    public ProductPanel(User user) {
        this.user = user;

        setLayout(new BorderLayout(12, 12));
        setBackground(new Color(14, 26, 42));   // Dark theme
        setBorder(BorderFactory.createEmptyBorder(12, 12, 12, 12));

        // --- Header ---
        JPanel top = new JPanel(new BorderLayout());
        top.setOpaque(false);

        JLabel title = new JLabel("Products", SwingConstants.LEFT);
        title.setFont(UIConstants.H2);
        title.setForeground(Color.WHITE);        // Title color
        top.add(title, BorderLayout.WEST);

        ModernButton refresh = new ModernButton("Refresh");
        refresh.addActionListener(e -> loadProducts());
        top.add(refresh, BorderLayout.EAST);

        add(top, BorderLayout.NORTH);

        // --- Product grid ---
        gridPanel = new JPanel(new WrapLayout(FlowLayout.LEFT, 16, 16));
        gridPanel.setBackground(new Color(14, 26, 42)); // dark background

        JScrollPane scroll = new JScrollPane(gridPanel);
        scroll.setBorder(null);
        scroll.getVerticalScrollBar().setUnitIncrement(16);
        scroll.getViewport().setBackground(new Color(14, 26, 42));
        add(scroll, BorderLayout.CENTER);

        SwingUtilities.invokeLater(this::loadProducts);
    }

    /** Loads all products initially */
    private void loadProducts() {
        try {
            List<Product> products = DataManager.getAllProducts();
            showProducts(products);
        } catch (Exception e) {
            e.printStackTrace();
            gridPanel.removeAll();

            JLabel err = new JLabel("Error loading products", SwingConstants.CENTER);
            err.setFont(UIConstants.REGULAR);
            err.setForeground(Color.WHITE);

            gridPanel.add(err);
            refreshView();
        }
    }

    /** Displays any list of products, including search results */
    public void showProducts(List<Product> products) {
        gridPanel.removeAll();

        if (products == null || products.isEmpty()) {
            JLabel noResults = new JLabel("No products found.", SwingConstants.CENTER);
            noResults.setFont(UIConstants.REGULAR);
            noResults.setForeground(Color.WHITE);
            gridPanel.add(noResults);
        } else {
            for (Product p : products) {
                try {
                    ProductCard card = new ProductCard(
                            p,
                            user instanceof Customer,
                            e -> {
                                if (user instanceof Customer customer) {
                                    try {
                                        customer.getCart().addProduct(p);
                                        DataManager.saveProducts();
                                        JOptionPane.showMessageDialog(this, p.getName() + " added to cart!");
                                    } catch (OutOfStockException ignored) {}
                                }
                            }
                    );

                    // Dark theme card
                    card.setBackground(new Color(24, 38, 56));
                    card.setBorder(BorderFactory.createLineBorder(new Color(70, 90, 110)));

                    // Make all texts inside ProductCard white
                    setAllTextWhite(card);

                    gridPanel.add(card);

                } catch (Exception ex) {
                    System.err.println("Error displaying product: " + p.getName());
                    ex.printStackTrace();
                }
            }
        }

        refreshView();
    }

    /** Ensures ALL labels inside card are white */
    private void setAllTextWhite(Component comp) {
        if (comp instanceof JLabel label) {
            label.setForeground(Color.WHITE);
        }

        if (comp instanceof JPanel panel) {
            panel.setOpaque(false); // prevents gray patches
            for (Component child : panel.getComponents()) {
                setAllTextWhite(child);
            }
        }
    }

    /** Refresh */
    private void refreshView() {
        gridPanel.revalidate();
        gridPanel.repaint();
    }
}
