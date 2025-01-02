"""
    path('', views.home, name='home')
    path('', Home.as_view(), name='home')
    path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from payments.views import InvoicePaymentData, v_invoicepayment_create, v_payment_create, v_payment_list, v_pending_payment_of_company

app_name = "payments"

urlpatterns = [
    path("", v_payment_list, name="payment_list"),
    path("create/", v_payment_create, name="payment_create"),
    path("invoice/create/", v_invoicepayment_create, name="invoicepayment_create"),
    path("payment/<int:pk>/", v_pending_payment_of_company, name="payment_pending"),
    path("payment/api/", InvoicePaymentData.as_view(), name="invoicepayment_api"),
]
