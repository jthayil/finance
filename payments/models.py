from django.db.models import (
    Model,
    DateTimeField,
    ForeignKey,
    BooleanField,
    FileField,
    IntegerField,
    CASCADE,
    FloatField,
    PositiveSmallIntegerField,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from invoices.models import Invoices
from masters.models import Company


class Payments(Model):
    user = ForeignKey(User, on_delete=CASCADE, null=False, blank=False)
    received_amt = FloatField(default=0)
    utr_file = FileField(upload_to="utr")
    buyer_id = ForeignKey(Company, on_delete=CASCADE, null=False, blank=False)
    deleted = BooleanField(default=False)
    status = PositiveSmallIntegerField(default=0)
    inserted_On = DateTimeField(auto_now_add=True)
    updated_On = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-id"]


class InvoicePayments(Model):
    payment_id = ForeignKey(Payments, on_delete=CASCADE, null=False, blank=False)
    invoice_id = ForeignKey(Invoices, on_delete=CASCADE, null=False, blank=False)
    allocated_amt = FloatField(default=0)
    tds_percent = PositiveSmallIntegerField()
    inserted_On = DateTimeField(auto_now_add=True)
    updated_On = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        verbose_name = "Invoice Payment"
        verbose_name_plural = "Invoice Payments"
        ordering = ["-id"]


@receiver(post_save, sender=InvoicePayments)
def update_received_amt(sender, instance, created, **kwargs):
    if created:
        payment = instance.payment_id
        payment.received_amt += instance.allocated_amt
        payment.save(update_fields=["received_amt"])
