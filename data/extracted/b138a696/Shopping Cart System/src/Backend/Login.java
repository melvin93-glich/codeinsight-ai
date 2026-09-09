package Backend;

public class Login {

    private Login() {}  // Private constructor to prevent instantiation

    public static User authenticate(String username, String password) {
        return DataManager.getUser(username, password);
    }

    /**
     * Registers a new user into the system.
     *
     * @param username The username for login
     * @param password The password for login
     * @param fullName The full name of the user
     * @param email The email of the user
     * @param role The role of the user (CUSTOMER, PREMIUM, or ADMIN)
     * @return true if user created successfully, false if username already exists
     */
    public static boolean createUser(String username, String password, String fullName, String email, Role role) {
        // Check if username already exists
        User existingUser = DataManager.getUser(username, password);
        if (existingUser != null) {
            return false; // User already exists
        }

        User newUser;
        switch (role) {
            case CUSTOMER -> newUser = new Customer(username, password, fullName, email);
            case PREMIUM -> newUser = new PremiumUser(username, password, fullName, email);
            case ADMIN -> newUser = new Admin(username, password, fullName, email);
            default -> throw new IllegalArgumentException("Invalid role: " + role);
        }

        // Add new user to DataManager
        DataManager.addUser(newUser);
        return true;
    }
}
