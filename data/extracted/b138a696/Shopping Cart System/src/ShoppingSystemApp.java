import javax.swing.*;

import GUI.LoginFrame;

public class ShoppingSystemApp {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(LoginFrame::new);
    }
}