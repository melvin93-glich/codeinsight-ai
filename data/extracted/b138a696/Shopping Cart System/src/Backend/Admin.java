package Backend;

import Exceptions.ProductNotFoundException;

public class Admin extends User {
    public Admin(String username, String password, String fullName, String email) {
        super(username, password, fullName, email, Role.ADMIN);
    }

    public void addProduct(Product product) {
        DataManager.addProduct(product);
    }

    public void removeProduct(String productId) throws ProductNotFoundException {
        DataManager.removeProduct(productId);
    }

    public void updateProductQuantity(String productId, int newQuantity) throws ProductNotFoundException {
        DataManager.updateProductQuantity(productId, newQuantity);
    }

    @Override
    public void performAction(){}
}