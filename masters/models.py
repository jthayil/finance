from django.db.models import (
    Model,
    DateTimeField,
    ForeignKey,
    CharField,
    BooleanField,
    CASCADE,
    FloatField,
    TextField,
    EmailField,
    IntegerField,
    ImageField,
)


class Pincodes(Model):
    pincode = IntegerField(null=False, blank=False)
    city = CharField(max_length=250, null=False, blank=False)
    state = CharField(max_length=250, null=False, blank=False)
    country = CharField(max_length=250, default="India", null=True, blank=True)
    inserted_On = DateTimeField(auto_now_add=True)
    updated_On = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.pincode)

    class Meta:
        verbose_name = "Pincode"
        verbose_name_plural = "Pincodes"
        ordering = ["state", "city"]
        unique_together = ["pincode", "city", "state"]


class Company(Model):
    name = CharField(max_length=250, null=False, blank=False)
    address = TextField()
    pincode = ForeignKey(Pincodes, on_delete=CASCADE, null=True, blank=True)
    gstin = CharField(max_length=250, null=False, blank=False)
    mobile = CharField(max_length=10, null=True, blank=True)
    email = EmailField(null=True, blank=True)
    pan = CharField(max_length=10, null=True, blank=True)
    state = CharField(max_length=128, null=False, blank=False)
    bank = CharField(max_length=250, null=True, blank=True)
    bank_account_holder = CharField(max_length=250, null=True, blank=True)
    bank_no = CharField(max_length=250, null=True, blank=True)
    bank_ifsc = CharField(max_length=250, null=True, blank=True)
    bank_branch = TextField(null=True, blank=True)
    provider = BooleanField(default=False)
    deleted = BooleanField(default=False)
    inserted_On = DateTimeField(auto_now_add=True)
    updated_On = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]


class HSN(Model):
    hsn_code = CharField(max_length=250, null=False, blank=False)
    description = TextField()
    inserted_On = DateTimeField(auto_now_add=True)
    updated_On = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(f"{self.id} ( {self.hsn_code} )")

    class Meta:
        verbose_name = "HSN"
        verbose_name_plural = "HSN"
        ordering = ["hsn_code"]


class Inventory(Model):
    name = CharField(max_length=250, null=False, blank=False)
    description = TextField(null=True, blank=True)
    rate = FloatField(null=True, blank=True)
    qty = FloatField(null=True, blank=True)
    min_stock = FloatField(default=float(0), null=True, blank=True)
    sgst = FloatField(null=True, blank=True)
    cgst = FloatField(null=True, blank=True)
    igst = FloatField(null=True, blank=True)
    hsn_id = ForeignKey(HSN, on_delete=CASCADE, null=True, blank=True)
    img = ImageField(upload_to="inventory", null=True, blank=True)
    deleted = BooleanField(default=False)
    inserted_On = DateTimeField(auto_now_add=True)
    updated_On = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"
        ordering = ["hsn_id"]
