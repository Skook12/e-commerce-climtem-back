from enum import Enum


class OrderStatus(Enum):
    Payment_Pending = "Pagamento pendente"
    Paid = "Pago"
    In_Transport = "Em transporte"
    Finalized = "Finalizado"

class PaymentType(Enum):
    PIX = "PIX"
    DEBIT_CARD = "Cartao de debito"
    CREDIT_CARD = "Cartao de credito"
    PAYMENT_SLIP = "Boleto"