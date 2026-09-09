package Backend;

import Exceptions.PaymentFailedException;

public class CreditCardPayment extends Payment {

    public CreditCardPayment() {}

    @Override
    public boolean processPayment(double amount) throws PaymentFailedException {
        // Simulate payment
        if (Math.random() < 0.1) {  // 10% failure rate
            throw new PaymentFailedException("Credit card payment failed.");
        }
        return true;
    }
}