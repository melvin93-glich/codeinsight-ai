package Backend;

import Exceptions.PaymentFailedException;

public abstract class Payment {
    public abstract boolean processPayment(double amount) throws PaymentFailedException;
}