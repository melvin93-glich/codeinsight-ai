package GUI;

import Backend.*;
import Exceptions.PaymentFailedException;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;
import java.text.SimpleDateFormat;
import java.util.Date;

public class PaymentPanel extends JDialog {
    private final User user;
    private final CartPanel cartPanel;

    public PaymentPanel(User user, CartPanel cartPanel) {
        this.user = user;
        this.cartPanel = cartPanel;

        setTitle("Payment");
        setSize(380, 220);
        setModal(true);
        setLocationRelativeTo(null);
        setLayout(new GridLayout(3, 1, 10, 10));
        getContentPane().setBackground(UIConstants.BG_LIGHT);
        setResizable(false);

        add(createButton("Pay via UPI", new UPIListener()));
        add(createButton("Pay with Credit Card", new CreditListener()));
        add(createButton("Cash on Delivery", e -> processCOD()));

        setVisible(true);
    }

    private JButton createButton(String text, ActionListener listener) {
        ModernButton b = new ModernButton(text);
        b.addActionListener(listener);
        return b;
    }

    private void processPayment(Payment payment) {
        try {
            if (user instanceof Customer customer) {

                double total = customer.calculateTotal();

                // ---- Process Payment ----
                payment.processPayment(total);

                // ---- Prepare Order Details ----
                int nextSerialNumber = DataManager.getUserOrders(user.getUsername()).size() + 1;
                String itemDetails = customer.getCart().getItems().toString();
                double totalCost = total;

                String currentTimestampString =
                        new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());

                // ---- Create Order ----
                Order order = new Order(
                        nextSerialNumber,
                        user.getUsername(),
                        itemDetails,
                        totalCost,
                        currentTimestampString
                );

                // ---- Save to DataManager ----
                DataManager.addOrder(order);

                // ---- Generate Bill ----
                String path = BillGenerator.generateBill(user, customer.getCart().getItems(), total);

                // ---- Clear cart ----
                customer.getCart().clear();
                cartPanel.refreshCart();

                JOptionPane.showMessageDialog(this, "Payment successful! Bill: " + path);
            }
            dispose();
        } catch (PaymentFailedException ex) {
            JOptionPane.showMessageDialog(this, ex.getMessage(), "Payment failed", JOptionPane.ERROR_MESSAGE);
        } catch (RuntimeException ex) {
            JOptionPane.showMessageDialog(this, "Error: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void processCOD() {
        if (user instanceof Customer customer) {

            double total = customer.calculateTotal();

            // ---- Prepare Order Details ----
            int nextSerialNumber = DataManager.getUserOrders(user.getUsername()).size() + 1;
            String itemDetails = customer.getCart().getItems().toString();
            double totalCost = total;

            String currentTimestampString =
                    new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());

            // ---- Create Order ----
            Order order = new Order(
                    nextSerialNumber,
                    user.getUsername(),
                    itemDetails,
                    totalCost,
                    currentTimestampString
            );

            // ---- Save Order ----
            DataManager.addOrder(order);

            // ---- Generate bill ----
            String path = BillGenerator.generateBill(user, customer.getCart().getItems(), total);

            // ---- Clear cart ----
            customer.getCart().clear();
            cartPanel.refreshCart();

            JOptionPane.showMessageDialog(this, "COD confirmed! Bill: " + path);
        }
        dispose();
    }

    private class UPIListener implements ActionListener {
        @Override
        public void actionPerformed(java.awt.event.ActionEvent e) {
            String upi = JOptionPane.showInputDialog("Enter UPI ID:");

            if (upi == null || upi.isBlank()) {
                JOptionPane.showMessageDialog(null, "UPI ID cannot be empty.", "Error", JOptionPane.WARNING_MESSAGE);
                return;
            }

            // If you want to validate format (optional)
            if (!upi.contains("@")) {
                JOptionPane.showMessageDialog(null, "Invalid UPI ID.", "Error", JOptionPane.WARNING_MESSAGE);
                return;
            }

            // Calls your PaymentPanel.processPayment(new UPIpayment())
            processPayment(new UPIpayment());
        }
    }


    private class CreditListener implements ActionListener {
        @Override
        public void actionPerformed(java.awt.event.ActionEvent e) {
            String card = JOptionPane.showInputDialog("Card number:");
            String exp = JOptionPane.showInputDialog("Expiry (MM/YY):");
            String cvv = JOptionPane.showInputDialog("CVV:");
            if (card != null && exp != null && cvv != null) processPayment(new CreditCardPayment());
        }
    }
}
