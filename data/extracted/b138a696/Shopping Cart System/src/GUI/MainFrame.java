package GUI;

import Backend.*;

import javax.swing.*;
import java.awt.*;

public class MainFrame extends JFrame {
    private final User user;

    public MainFrame(User user) {
        this.user = user;

        setTitle("Shopping System - " + user.getFullName());
        setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        setSize(1100, 720);
        setLocationRelativeTo(null);
        getContentPane().setBackground(new Color(14, 26, 42)); // Dark theme

        // Force tab text color to white globally
        UIManager.put("TabbedPane.selectedForeground", Color.WHITE);
        UIManager.put("TabbedPane.foreground", Color.WHITE);
        UIManager.put("TabbedPane.focus", Color.WHITE);

        JTabbedPane tabs = new JTabbedPane();
        tabs.setFont(UIConstants.REGULAR);
        tabs.setBackground(new Color(24, 38, 56));  // Tab bar
        tabs.setForeground(Color.WHITE);            // Text color
        
        // Also ensure selected tab text stays white
        tabs.setUI(new javax.swing.plaf.basic.BasicTabbedPaneUI() {
            @Override
            protected void installDefaults() {
                super.installDefaults();
                highlight = new Color(24, 38, 56);   // fix highlight color
                lightHighlight = new Color(24, 38, 56);
                shadow = new Color(24, 38, 56);
                darkShadow = new Color(24, 38, 56);
            }

            @Override
            protected void paintText(Graphics g, int tabPlacement, Font font,
                                     FontMetrics metrics, int tabIndex,
                                     String title, Rectangle textRect, boolean isSelected) {
                g.setFont(font);
                g.setColor(Color.WHITE);   // <-- FORCE white text
                g.drawString(title, textRect.x, textRect.y + metrics.getAscent());
            }
        });

        ProductPanel productPanel = new ProductPanel(user);
        SearchPanel searchPanel = new SearchPanel(user);

        tabs.addTab("Home", productPanel);
        tabs.addTab("Search", searchPanel);
        tabs.addTab("Suggestions", new SuggestionsPanel(user));
        tabs.addTab("Cart", new CartPanel(user));
        tabs.addTab("Order History", new OrderHistoryPanel(user.getUsername()));

        if (user.getRole() == Role.ADMIN) {
            tabs.addTab("Admin", new AdminPanel());
        }

        add(tabs);
        setVisible(true);
    }
}
