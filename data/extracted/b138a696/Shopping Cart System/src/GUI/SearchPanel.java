package GUI;

import Backend.*;
import Exceptions.OutOfStockException;

import javax.swing.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import java.awt.*;
import java.util.List;

public class SearchPanel extends JPanel {

    private JTextField searchField;
    private JPanel resultsPanel;
    private User user;

    public SearchPanel(User user) {
        this.user = user;

        setLayout(new BorderLayout(10,10));
        setBackground(new Color(14, 26, 42)); // Dark theme
        setBorder(BorderFactory.createEmptyBorder(12,12,12,12));

        JPanel topPanel = new JPanel(new BorderLayout(5,5));
        topPanel.setOpaque(false);

        searchField = new JTextField();
        searchField.setPreferredSize(new Dimension(300, 30));
        searchField.setFont(UIConstants.REGULAR);
        searchField.setBackground(new Color(236, 236, 236));
        searchField.setForeground(Color.BLACK);

        ModernButton searchBtn = new ModernButton("Search");
        searchBtn.addActionListener(e -> searchProducts());

        topPanel.add(searchField, BorderLayout.CENTER);
        topPanel.add(searchBtn, BorderLayout.EAST);

        add(topPanel, BorderLayout.NORTH);

        resultsPanel = new JPanel();
        resultsPanel.setLayout(new WrapLayout(FlowLayout.LEFT, 16, 16));
        resultsPanel.setBackground(new Color(14, 26, 42));

        JScrollPane scrollPane = new JScrollPane(resultsPanel);
        scrollPane.setBorder(null);
        scrollPane.getViewport().setBackground(new Color(14, 26, 42));
        add(scrollPane, BorderLayout.CENTER);

        searchField.getDocument().addDocumentListener(new DocumentListener() {
            @Override public void insertUpdate(DocumentEvent e) { searchProducts(); }
            @Override public void removeUpdate(DocumentEvent e) { searchProducts(); }
            @Override public void changedUpdate(DocumentEvent e) { searchProducts(); }
        });

        showMessage("Type something to search...");
    }

    private void showMessage(String message) {
        resultsPanel.removeAll();
        resultsPanel.setLayout(new BorderLayout());
        JLabel label = new JLabel(message, SwingConstants.CENTER);
        label.setFont(UIConstants.REGULAR);
        label.setForeground(Color.WHITE); // white text
        resultsPanel.add(label, BorderLayout.CENTER);
        resultsPanel.revalidate();
        resultsPanel.repaint();
    }

    private void searchProducts() {
        String query = searchField.getText().trim();

        if (query.isEmpty()) {
            showMessage("Type something to search...");
            return;
        }

        List<Product> results = SearchProducts.searchByName(query);

        resultsPanel.removeAll();
        resultsPanel.setLayout(new WrapLayout(FlowLayout.LEFT, 16,16));

        if (results.isEmpty()) {
            showMessage("No products found for: " + query);
        } else {
            for (Product p : results) {
                JPanel card = new JPanel(new BorderLayout());
                card.setBorder(BorderFactory.createLineBorder(new Color(70, 90, 110)));
                card.setBackground(new Color(24, 38, 56)); // card bg
                card.setPreferredSize(new Dimension(180, 220));

                JLabel imgLabel = new JLabel();
                ImageIcon icon = new ImageIcon(p.getImagePath());
                Image img = icon.getImage().getScaledInstance(160, 120, Image.SCALE_SMOOTH);
                imgLabel.setIcon(new ImageIcon(img));
                imgLabel.setHorizontalAlignment(SwingConstants.CENTER);
                card.add(imgLabel, BorderLayout.NORTH);

                JPanel info = new JPanel(new GridLayout(0,1));
                info.setOpaque(false);

                JLabel nameL = new JLabel(p.getName(), SwingConstants.CENTER);
                nameL.setForeground(Color.WHITE);

                JLabel priceL = new JLabel("₹" + p.getPrice(), SwingConstants.CENTER);
                priceL.setForeground(Color.WHITE);

                JLabel catL = new JLabel("Category: " + p.getCategory(), SwingConstants.CENTER);
                catL.setForeground(new Color(220, 220, 220));

                info.add(nameL);
                info.add(priceL);
                info.add(catL);

                card.add(info, BorderLayout.CENTER);

                if (user instanceof Customer customer) {
                    ModernButton addBtn = new ModernButton("Add to Cart");
                    addBtn.addActionListener(e -> {
                        try {
                            customer.getCart().addProduct(p);
                            DataManager.saveProducts();
                            JOptionPane.showMessageDialog(this, "Added to cart");
                        } catch (OutOfStockException ex) {
                            JOptionPane.showMessageDialog(this, ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
                        }
                    });
                    card.add(addBtn, BorderLayout.SOUTH);
                }

                resultsPanel.add(card);
            }
        }

        resultsPanel.revalidate();
        resultsPanel.repaint();
    }
}
