package Backend;

import Exceptions.PaymentFailedException;

public class UPIpayment extends Payment {

    public UPIpayment() {}

    @Override
    public boolean processPayment(double amount) throws PaymentFailedException {

        if (amount > 40000) {
            throw new PaymentFailedException("Payment exceeded limit.");
        }

        // Simulate payment failure
        if (Math.random() < 0.1) {
            throw new PaymentFailedException("UPI payment failed.");
        }

        return true;
    }
}
