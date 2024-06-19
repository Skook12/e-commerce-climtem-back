from enum import Enum


class OrderStatus(Enum):
    Payment_Pending = "Pagamento pendente"
    Paid = "Pago"
    In_Transport = "Em transporte"
    Finalized = "Finalizado"

class PaymentType(Enum):
    PIX = "pix"
    DEBIT = "debito"
    CREDIT = "credito"
    PAYMENT_SLIP = "boleto"