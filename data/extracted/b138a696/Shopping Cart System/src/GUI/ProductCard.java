package GUI;

import Backend.Product;

import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;

public class ProductCard extends JPanel {
    public static final int THUMB = 150;

    public ProductCard(Product p, boolean showAddButton, java.awt.event.ActionListener addListener) {
        setLayout(new BorderLayout(8, 8));
        setBackground(new Color(24, 38, 56));   // Dark card background
        setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(70, 90, 110), 1, true),
                BorderFactory.createEmptyBorder(10, 10, 10, 10)
        ));
        setPreferredSize(new Dimension(220, 280));

        // ---------- IMAGE ----------
        JLabel img = new JLabel();
        img.setHorizontalAlignment(SwingConstants.CENTER);

        try {
            ImageIcon ic = new ImageIcon(p.getImagePath());
            Image scaled = getScaledImage(ic.getImage(), THUMB, THUMB);
            img.setIcon(new ImageIcon(scaled));
        } catch (Exception ignored) {
            img.setText("No Image");
            img.setForeground(Color.WHITE);  // white fallback text
        }

        add(img, BorderLayout.CENTER);

        // ---------- INFO PANEL ----------
        JPanel info = new JPanel(new GridLayout(0, 1));
        info.setOpaque(false);

        JLabel name = new JLabel("<html><b>" + p.getName() + "</b></html>", SwingConstants.CENTER);
        name.setFont(UIConstants.REGULAR);
        name.setForeground(Color.WHITE); // WHITE NAME

        JLabel price = new JLabel("₹ " + p.getPrice(), SwingConstants.CENTER);
        price.setFont(UIConstants.BOLD);
        price.setForeground(Color.WHITE); // WHITE PRICE

        info.add(name);
        info.add(price);

        add(info, BorderLayout.NORTH);

        // ---------- ADD TO CART BUTTON ----------
        if (showAddButton) {
            ModernButton add = new ModernButton("Add to Cart");
            add.addActionListener(addListener);

            JPanel bottom = new JPanel(new FlowLayout(FlowLayout.CENTER));
            bottom.setOpaque(false);
            bottom.add(add);

            add(bottom, BorderLayout.SOUTH);
        }
    }

    private Image getScaledImage(Image srcImg, int maxW, int maxH) {
        if (srcImg == null) 
            return new BufferedImage(maxW, maxH, BufferedImage.TYPE_INT_ARGB);

        int w = srcImg.getWidth(null);
        int h = srcImg.getHeight(null);
        if (w <= 0 || h <= 0) return srcImg;

        double scale = Math.min((double) maxW / w, (double) maxH / h);
        int nw = (int) (w * scale);
        int nh = (int) (h * scale);

        return srcImg.getScaledInstance(nw, nh, Image.SCALE_SMOOTH);
    }
}
