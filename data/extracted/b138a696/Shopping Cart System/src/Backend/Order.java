package Backend;

public class Order {
    private final int sNo;
    private final String username;
    private final String item;
    private final double cost;
    private final String time; // Can be Date or String

    public Order(int sNo, String username, String item, double cost, String time) {
        this.sNo = sNo;
        this.username = username;
        this.item = item;
        this.cost = cost;
        this.time = time;
    }

    public int getSNo() { return sNo; }
    public String getUsername() { return username; }
    public String getItem() { return item; }
    public double getCost() { return cost; }
    public String getTime() { return time; }
}
