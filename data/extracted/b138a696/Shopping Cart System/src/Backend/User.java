package Backend;

import java.io.Serializable;

public abstract class User implements Serializable {
    protected final String username;
    protected final String password;
    protected final String fullName;
    protected final String email;
    protected Role role;  // Removed final to allow subclass override

    public User(String username, String password, String fullName, String email, Role role) {
        this.username = username;
        this.password = password;
        this.fullName = fullName;
        this.email = email;
        this.role = role;
    }

    // Getters
    public String getUsername() { return username; }
    public String getFullName() { return fullName; }
    public String getEmail(){return email;}
    public Role getRole() { return role; }

    public void performAction() {
        // Placeholder for role-specific actions; to be implemented in subclasses if needed
    }
}