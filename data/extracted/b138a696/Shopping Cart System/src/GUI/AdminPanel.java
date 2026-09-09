package GUI;

import Backend.*;
import javax.swing.*;
import java.awt.*;

public class AdminPanel extends JPanel {
    public AdminPanel() {
        setBackground(UIConstants.BG_LIGHT);
        setLayout(new GridBagLayout());
        setBorder(BorderFactory.createEmptyBorder(12,12,12,12));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(8,8,8,8);
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.gridx = 0; gbc.gridy = 0;

        JLabel title = new JLabel("Admin - Add Product", SwingConstants.CENTER);
        title.setFont(UIConstants.H2);
        gbc.gridwidth = 2;
        add(title, gbc);

        gbc.gridwidth = 1;
        gbc.gridy++;
        add(new JLabel("Name:"), gbc);
        JTextField name = new JTextField();
        gbc.gridx = 1;
        add(name, gbc);

        gbc.gridx = 0; gbc.gridy++;
        add(new JLabel("Product ID:"), gbc);
        JTextField pid = new JTextField();
        gbc.gridx = 1;
        add(pid, gbc);

        gbc.gridx = 0; gbc.gridy++;
        add(new JLabel("Price:"), gbc);
        JTextField price = new JTextField();
        gbc.gridx = 1;
        add(price, gbc);

        gbc.gridx = 0; gbc.gridy++; gbc.gridwidth = 2;
        ModernButton addBtn = new ModernButton("Add Product");
        add(addBtn, gbc);

        addBtn.addActionListener(e -> {
            String n = name.getText().trim(), id = pid.getText().trim(), ptext = price.getText().trim();
            try {
                double pr = Double.parseDouble(ptext);
                Product product = new Product(0, n, id, pr, 10, "Category", "Brand", "Desc", 5, "data/images/default.png");
                DataManager.addProduct(product);
                JOptionPane.showMessageDialog(this, "Added successfully");
                name.setText(""); pid.setText(""); price.setText("");
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Price must be numeric", "Invalid input", JOptionPane.ERROR_MESSAGE);
            } catch (RuntimeException ex) {
                JOptionPane.showMessageDialog(this, "Error: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
            }
        });
    }
}
