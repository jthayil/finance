from fms.support import convert_to_words
from django.db.models import (
    Model,
    DateTimeField,
    ForeignKey,
    SmallIntegerField,
    CharField,
    BooleanField,
    Case,
    When,
    Value,
    Func,
    CASCADE,
    FloatField,
    PositiveSmallIntegerField,
    Sum,
    ExpressionWrapper,
    F,
)
from django.contrib.auth.models import User
from masters.models import Company, Inventory


class Invoices(Model):
    user = ForeignKey(User, on_delete=CASCADE, null=False, blank=False)
    invoice_no = SmallIntegerField(null=False, blank=False)
    buyer = ForeignKey(Company, on_delete=CASCADE, null=False, blank=False)
    shipTo = ForeignKey(
        Company, related_name="ship_to", on_delete=CASCADE, null=False, blank=False
    )
    deleted = BooleanField(default=False)
    discount = PositiveSmallIntegerField(default=0)
    status = PositiveSmallIntegerField(default=0)
    inserted_On = DateTimeField(auto_now_add=True)
    updated_On = DateTimeField(auto_now=True)

    def invoice_total(self) -> float:
        return sum(
            item.taxable_amount()
            for item in InvoiceItems.objects.filter(invoice_id=self.id)
        )

    def invoice_qty(self) -> int:
        return (
            InvoiceItems.objects.filter(invoice_id=self.id).aggregate(total=Sum("qty"))[
                "total"
            ]
            or 0
        )

    def tax_def(self):
        l_tax_amt = (
            InvoiceItems.objects.filter(invoice_id=self.id)
            .values("cgst", "sgst", "igst")
            .annotate(
                cgst_amt=Case(
                    When(cgst=0, then=Value(0)),
                    default=Func(
                        ExpressionWrapper(
                            Sum(F("qty") * F("rate")) * (F("cgst") / 100),
                            output_field=FloatField(),
                        ),
                        function="ROUND",
                        template="%(function)s(%(expressions)s)",
                        output_field=FloatField(),
                    ),
                    output_field=FloatField(),
                ),
                sgst_amt=Case(
                    When(sgst=0, then=Value(0)),
                    default=Func(
                        ExpressionWrapper(
                            Sum(F("qty") * F("rate")) * (F("sgst") / 100),
                            output_field=FloatField(),
                        ),
                        function="ROUND",
                        template="%(function)s(%(expressions)s)",
                        output_field=FloatField(),
                    ),
                    output_field=FloatField(),
                ),
                igst_amt=Case(
                    When(igst=0, then=Value(0)),
                    default=Func(
                        ExpressionWrapper(
                            Sum(F("qty") * F("rate")) * (F("igst") / 100),
                            output_field=FloatField(),
                        ),
                        function="ROUND",
                        template="%(function)s(%(expressions)s)",
                        output_field=FloatField(),
                    ),
                    output_field=FloatField(),
                ),
            )
            .order_by("cgst", "sgst", "igst")
        )
        new_tax_amt_dict = []
        for x in l_tax_amt:
            if x["sgst"] > 0:
                new_tax_amt_dict.append(
                    {f"SGST @{(int(x['sgst']))}%": f"{x['sgst_amt']}"}
                )
            if x["cgst"] > 0:
                new_tax_amt_dict.append(
                    {f"CGST @{(int(x['cgst']))}%": f"{x['cgst_amt']}"}
                )
            if x["igst"] > 0:
                new_tax_amt_dict.append(
                    {f"IGST @{(int(x['igst']))}%": f"{x['igst_amt']}"}
                )
        return new_tax_amt_dict

    def invoice_tax(self):
        return sum(
            item.tax_amt() for item in InvoiceItems.objects.filter(invoice_id=self.id)
        )

    def invoice_total_amt(self):
        res = sum(
            item.total_amount()
            for item in InvoiceItems.objects.filter(invoice_id=self.id)
        )
        return float(res).__round__(2)

    def invoice_total_in_words(self):
        return convert_to_words(self.invoice_total_amt())

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        verbose_name = "Invoices"
        verbose_name_plural = "Invoices"
        ordering = ["-id"]


class InvoiceItems(Model):
    invoice_id = ForeignKey(Invoices, on_delete=CASCADE, null=False, blank=False)
    inventory_id = ForeignKey(Inventory, on_delete=CASCADE, null=True, blank=True)
    item = CharField(max_length=250, null=False, blank=True)
    sgst = FloatField(default=float(0))
    cgst = FloatField(default=float(0))
    igst = FloatField(default=float(0))
    rate = FloatField(null=False, blank=True)
    qty = FloatField(null=False, blank=True)
    discount = PositiveSmallIntegerField(default=0)
    deleted = BooleanField(default=False)
    inserted_On = DateTimeField(auto_now_add=True)
    updated_On = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id)
    
    def qty_rate(self)->float:
        return self.rate * self.qty
    
    def discount_amt(self)->float:
        return round(self.qty_rate() * (self.discount / 100), 2)

    def taxable_amount(self) -> float:
        return round(self.qty_rate() - self.discount_amt(), 2)

    def tax(self) -> float:
        return self.sgst + self.cgst + self.igst

    def sgst_tax_amt(self) -> float:
        return (self.sgst / 100) * self.taxable_amount

    def cgst_tax_amt(self) -> float:
        return (self.cgst / 100) * self.taxable_amount

    def igst_tax_amt(self) -> float:
        return (self.igst / 100) * self.taxable_amount

    def tax_amt(self) -> float:
        amt = self.taxable_amount()
        tax = self.tax()
        return round((tax / 100) * amt, 2)

    def total_amount(self) -> float:
        amt = self.taxable_amount()
        tax_amt = self.tax_amt()
        return amt + tax_amt

    class Meta:
        verbose_name = "Invoice Item"
        verbose_name_plural = "Invoice Items"
        ordering = ["-invoice_id"]
