package GUI;

import Backend.Login;
import Backend.Role;
import Backend.User;

import javax.swing.*;
import java.awt.*;

public class LoginFrame extends JFrame {

    private final JTextField usernameField = new JTextField(18);
    private final JPasswordField passwordField = new JPasswordField(18);

    private static class BackgroundPanel extends JPanel {
        private final Image backgroundImage;

        public BackgroundPanel(String imagePath) {
            backgroundImage = new ImageIcon(imagePath).getImage();
            setBackground(new Color(14, 26, 42)); // Dark blue tone
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            g.drawImage(backgroundImage, 0, 0, getWidth(), getHeight(), this);
        }
    }

    public LoginFrame() {
        setTitle("Shopping Cart - Login");
        setSize(480, 380);
        setLocationRelativeTo(null);
        setResizable(false);
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        BackgroundPanel bgPanel = new BackgroundPanel("static/assets/login_bg.jpg");
        bgPanel.setLayout(new GridBagLayout());
        setContentPane(bgPanel);

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(12, 12, 12, 12);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        JLabel title = new JLabel("Welcome! Please Login", SwingConstants.CENTER);
        title.setFont(UIConstants.H1);
        title.setForeground(Color.WHITE);   // Title color updated
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.gridwidth = 2;
        bgPanel.add(title, gbc);

        // USERNAME LABEL
        gbc.gridwidth = 1;
        gbc.gridy++;
        JLabel userLabel = new JLabel("Username:");
        userLabel.setForeground(new Color(220, 220, 220));  // Light gray
        bgPanel.add(userLabel, gbc);

        // USERNAME FIELD
        gbc.gridx = 1;
        usernameField.setFont(UIConstants.REGULAR);
        usernameField.setBackground(new Color(236, 236, 236)); // light gray input box
        usernameField.setForeground(Color.BLACK);
        bgPanel.add(usernameField, gbc);

        // PASSWORD LABEL
        gbc.gridx = 0;
        gbc.gridy++;
        JLabel passLabel = new JLabel("Password:");
        passLabel.setForeground(new Color(220, 220, 220)); // light gray
        bgPanel.add(passLabel, gbc);

        // PASSWORD FIELD
        gbc.gridx = 1;
        passwordField.setFont(UIConstants.REGULAR);
        passwordField.setBackground(new Color(236, 236, 236)); // light gray
        passwordField.setForeground(Color.BLACK);
        bgPanel.add(passwordField, gbc);

        // BUTTON PANEL
        gbc.gridx = 0;
        gbc.gridy++;
        gbc.gridwidth = 2;

        JPanel buttonPanel = new JPanel();
        buttonPanel.setOpaque(false);
        buttonPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 15, 0));

        ModernButton loginBtn = new ModernButton("Login");
        loginBtn.setPreferredSize(new Dimension(120, 40));
        buttonPanel.add(loginBtn);

        ModernButton signupBtn = new ModernButton("Sign Up");
        signupBtn.setPreferredSize(new Dimension(120, 40));
        buttonPanel.add(signupBtn);

        bgPanel.add(buttonPanel, gbc);

        loginBtn.addActionListener(e -> attemptLogin());
        signupBtn.addActionListener(e -> openSignupDialog());

        setVisible(true);
    }

    private void attemptLogin() {
        String u = usernameField.getText().trim();
        String p = new String(passwordField.getPassword());
        User user = Login.authenticate(u, p);

        if (user != null) {
            dispose();
            new MainFrame(user);
        } else {
            JOptionPane.showMessageDialog(this, "Invalid username or password",
                    "Login Failed", JOptionPane.ERROR_MESSAGE);
            passwordField.setText("");
        }
    }

    private void openSignupDialog() {
        JTextField username = new JTextField(15);
        JPasswordField password = new JPasswordField(15);
        JTextField fullname = new JTextField(15);
        JTextField email = new JTextField(15);
        JComboBox<Role> roleBox = new JComboBox<>(Role.values());

        JPanel panel = new JPanel(new GridLayout(0, 1, 5, 5));
        panel.setBackground(new Color(20, 32, 48)); // dialog background

        JLabel l1 = new JLabel("Full Name:");
        l1.setForeground(Color.WHITE);
        panel.add(l1);
        panel.add(fullname);

        JLabel l2 = new JLabel("Email:");
        l2.setForeground(Color.WHITE);
        panel.add(l2);
        panel.add(email);

        JLabel l3 = new JLabel("Username:");
        l3.setForeground(Color.WHITE);
        panel.add(l3);
        panel.add(username);

        JLabel l4 = new JLabel("Password:");
        l4.setForeground(Color.WHITE);
        panel.add(l4);
        panel.add(password);

        JLabel l5 = new JLabel("Role:");
        l5.setForeground(Color.WHITE);
        panel.add(l5);
        panel.add(roleBox);

        int result = JOptionPane.showConfirmDialog(
                this, panel, "Create New Account",
                JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE
        );

        if (result == JOptionPane.OK_OPTION) {
            String u = username.getText().trim();
            String p = new String(password.getPassword());
            String f = fullname.getText().trim();
            String e = email.getText().trim();
            Role r = (Role) roleBox.getSelectedItem();

            if (u.isEmpty() || p.isEmpty() || f.isEmpty() || e.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please fill all fields",
                        "Incomplete Data", JOptionPane.WARNING_MESSAGE);
                return;
            }

            boolean created = Login.createUser(u, p, f, e, r);
            if (created) {
                JOptionPane.showMessageDialog(this, "Account created successfully! You can now log in.",
                        "Success", JOptionPane.INFORMATION_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(this, "Username already exists! Choose another one.",
                        "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(LoginFrame::new);
    }
}
