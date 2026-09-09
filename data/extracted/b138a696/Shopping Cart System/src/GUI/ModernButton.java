package GUI;

import javax.swing.*;
import java.awt.*;

/**
 * Reusable modern rounded button used across panels.
 */
public class ModernButton extends JButton {
    public ModernButton(String text) {
        super(text);
        setFont(UIConstants.BOLD);
        setForeground(Color.WHITE);
        setBackground(UIConstants.PRIMARY);
        setFocusPainted(false);
        setBorderPainted(false);
        setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        setOpaque(false);
        setPreferredSize(new Dimension(140, 36));
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = (Graphics2D) g.create();
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        Color fill = getModel().isPressed() ? UIConstants.PRIMARY.darker()
                : getModel().isRollover() ? UIConstants.PRIMARY_HOVER
                : getBackground();

        g2.setColor(fill);
        g2.fillRoundRect(0, 0, getWidth(), getHeight(), 12, 12);

        // draw text centered
        g2.setFont(getFont());
        g2.setColor(getForeground());
        FontMetrics fm = g2.getFontMetrics();
        int textX = (getWidth() - fm.stringWidth(getText())) / 2;
        int textY = (getHeight() + fm.getAscent()) / 2 - 2;
        g2.drawString(getText(), textX, textY);

        g2.dispose();
    }

    @Override
    protected void paintBorder(Graphics g) {
        // no border
    }
}
