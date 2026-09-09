package GUI;

import Backend.*;
import javax.swing.*;
import java.awt.*;
import java.util.List;

public class CartPanel extends JPanel {
    private final User user;
    private final JPanel itemsPanel;

    public CartPanel(User user) {
        this.user = user;
        setLayout(new BorderLayout(12, 12));
        setBackground(new Color(14, 26, 42));   // Dark theme background
        setBorder(BorderFactory.createEmptyBorder(12, 12, 12, 12));

        JLabel title = new JLabel("Your Cart", SwingConstants.LEFT);
        title.setFont(UIConstants.H2);
        title.setForeground(Color.WHITE);       // Title color
        add(title, BorderLayout.NORTH);

        itemsPanel = new JPanel();
        itemsPanel.setLayout(new BoxLayout(itemsPanel, BoxLayout.Y_AXIS));
        itemsPanel.setBackground(new Color(14, 26, 42));   // same theme

        JScrollPane scroll = new JScrollPane(itemsPanel);
        scroll.setBorder(null);
        scroll.getViewport().setBackground(new Color(14, 26, 42));
        add(scroll, BorderLayout.CENTER);

        JPanel bottom = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        bottom.setOpaque(false);

        ModernButton checkout = new ModernButton("Checkout");
        ModernButton refresh = new ModernButton("Refresh");
        refresh.addActionListener(e -> refreshCart());
        checkout.addActionListener(e -> new PaymentPanel(user, this));

        bottom.add(refresh);
        bottom.add(checkout);
        add(bottom, BorderLayout.SOUTH);

        SwingUtilities.invokeLater(this::refreshCart);
    }

    public void refreshCart() {
        itemsPanel.removeAll();

        if (!(user instanceof Customer)) {
            JLabel msg = new JLabel("No cart - user is not a customer");
            msg.setForeground(Color.WHITE);
            itemsPanel.add(msg);
        } else {
            Customer c = (Customer) user;
            List<Product> items = c.getCart().getItems();

            if (items.isEmpty()) {
                JLabel empty = new JLabel("Your cart is empty", SwingConstants.CENTER);
                empty.setFont(UIConstants.REGULAR);
                empty.setForeground(Color.WHITE);
                itemsPanel.add(empty);
            } else {
                for (Product p : items) {
                    JPanel row = new JPanel(new BorderLayout(8, 8));
                    row.setBackground(new Color(24, 38, 56));   // Card background
                    row.setBorder(BorderFactory.createCompoundBorder(
                            BorderFactory.createLineBorder(new Color(70, 90, 110), 1, true),
                            BorderFactory.createEmptyBorder(8, 8, 8, 8)
                    ));

                    JLabel info = new JLabel(p.getName() + " - ₹ " + p.getPrice());
                    info.setFont(UIConstants.REGULAR);
                    info.setForeground(Color.WHITE);             // white text
                    row.add(info, BorderLayout.CENTER);

                    ModernButton remove = new ModernButton("Remove");
                    remove.setBackground(Color.RED);
                    remove.addActionListener(e -> {
                        c.getCart().removeProduct(p);
                        DataManager.saveProducts();
                        refreshCart();
                    });
                    row.add(remove, BorderLayout.EAST);

                    itemsPanel.add(row);
                    itemsPanel.add(Box.createRigidArea(new Dimension(0, 8)));
                }

                double total = c.calculateTotal();
                JLabel totalLbl = new JLabel("Total: ₹ " + total, SwingConstants.RIGHT);
                totalLbl.setFont(UIConstants.BOLD);
                totalLbl.setForeground(Color.WHITE);
                itemsPanel.add(totalLbl);
            }
        }

        itemsPanel.revalidate();
        itemsPanel.repaint();
    }
}
