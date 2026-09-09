package GUI;

import java.awt.Color;
import java.awt.Font;

public final class UIConstants {
    public static final String FONT_FAMILY = "Segoe UI";
    public static final Font H1 = new Font(FONT_FAMILY, Font.BOLD, 20);
    public static final Font H2 = new Font(FONT_FAMILY, Font.BOLD, 16);
    public static final Font REGULAR = new Font(FONT_FAMILY, Font.PLAIN, 14);
    public static final Font BOLD = new Font(FONT_FAMILY, Font.BOLD, 14);

    public static final Color BG_LIGHT = new Color(245, 247, 250);
    public static final Color CARD_BG = Color.WHITE;
    public static final Color PRIMARY = new Color(70, 120, 255);
    public static final Color PRIMARY_HOVER = new Color(80, 130, 255);
    public static final Color DANGER = new Color(240, 80, 80);
    public static final Color BORDER = new Color(225, 230, 235);

    private UIConstants() {}
}
