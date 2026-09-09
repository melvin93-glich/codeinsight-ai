package GUI;

import Backend.*;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.util.List;

public class OrderHistoryPanel extends JPanel {

    private final JTable table;
    private final DefaultTableModel model;
    private final String username;

    public OrderHistoryPanel(String username) {
        this.username = username;

        setLayout(new BorderLayout(10, 10));
        setBackground(new Color(14, 26, 42)); // same dark blue theme

        // ----------- TITLE -----------
        JLabel title = new JLabel("Order History", SwingConstants.CENTER);
        title.setFont(UIConstants.H2);
        title.setForeground(Color.WHITE);
        add(title, BorderLayout.NORTH);

        // ----------- TABLE -----------
        String[] columns = {"S.No", "Item", "Cost", "Time"};
        model = new DefaultTableModel(columns, 0);
        table = new JTable(model);

        table.setBackground(new Color(236, 236, 236));  // light gray table
        table.setForeground(Color.BLACK);
        table.setRowHeight(28);

        refreshTable();

        JScrollPane scrollPane = new JScrollPane(table);
        add(scrollPane, BorderLayout.CENTER);

        // ----------- REFRESH BUTTON -----------
        JPanel bottomPanel = new JPanel(new FlowLayout());
        bottomPanel.setBackground(new Color(14, 26, 42)); // match theme

        ModernButton refreshBtn = new ModernButton("Refresh");
        refreshBtn.setPreferredSize(new Dimension(120, 40));

        refreshBtn.addActionListener(e -> refreshTable());

        bottomPanel.add(refreshBtn);
        add(bottomPanel, BorderLayout.SOUTH);
    }

    // ----------------------------
    // Refresh orders dynamically
    // ----------------------------
    public void refreshTable() {
        model.setRowCount(0);

        List<Order> orders = DataManager.getUserOrders(username);

        for (Order o : orders) {
            model.addRow(new Object[]{
                    o.getSNo(),
                    o.getItem(),
                    String.format("%.2f", o.getCost()),
                    o.getTime()
            });
        }
    }
}
