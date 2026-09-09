package Backend;

import javax.imageio.ImageIO;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Creates a simple PNG bill image listing products and total.
 * Make sure User has getFullName() (or change to getUsername()).
 */
public final class BillGenerator {

    private static final Logger LOGGER = Logger.getLogger(BillGenerator.class.getName());

    private BillGenerator() {}

    /**
     * Generates a bill image and returns the generated file path.
     *
     * @param user  the user for whom the bill is generated (uses getFullName())
     * @param items list of Product items (if you need quantities, change type to Map<Product,Integer>)
     * @param total final total amount
     * @return path to generated PNG file
     */
    public static String generateBill(User user, List<Product> items, double total) {
        String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String dirPath = "data" + File.separator + "bills";
        String filePath = dirPath + File.separator + "bill_" + timestamp + ".png";

        int width = 500;
        int height = 200 + Math.max(0, items.size()) * 24;
        BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = image.createGraphics();

        try {
            g.setColor(Color.WHITE);
            g.fillRect(0, 0, width, height);

            g.setColor(Color.BLACK);
            g.setFont(new Font("Arial", Font.BOLD, 18));
            g.drawString("Shopping Cart Bill", 20, 30);

            g.setFont(new Font("Arial", Font.PLAIN, 12));
            String userName = (user != null && user.getFullName() != null) ? user.getFullName() : user.getUsername();
            g.drawString("User: " + userName, 20, 55);
            g.drawString("Date: " + new Date().toString(), 20, 75);

            int y = 105;
            for (Product p : items) {
                String line = String.format("%s - %.2f", p.getName(), p.getPrice());
                g.drawString(line, 20, y);
                y += 20;
            }

            g.setFont(new Font("Arial", Font.BOLD, 14));
            g.drawString(String.format("Total: %.2f", total), 20, y + 20);

        } finally {
            g.dispose();
        }

        try {
            File dir = new File(dirPath);
            if (!dir.exists()) {
                boolean ok = dir.mkdirs();
                if (!ok) {
                    LOGGER.log(Level.WARNING, "Could not create directory for bills: " + dirPath);
                }
            }
            ImageIO.write(image, "png", new File(filePath));
        } catch (IOException e) {
            LOGGER.log(Level.SEVERE, "Error generating bill: " + e.getMessage(), e);
        }

        return filePath;
    }
}
