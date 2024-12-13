"""
path('', views.home, name='home')
path('', Home.as_view(), name='home')
path('blog/', include('blog.urls'))
"""

from django.urls import path
from invoices.views import invoiceData, invoiceItemsData, v_dashboard, v_invoice_create, v_invoice_fingerpost, v_invoice_generate, v_invoice_item_create, v_invoice_item_delete, v_invoice_list, v_invoice_receipt, v_invoice_update, v_invoice_pdf

app_name = "invoices"


urlpatterns = [
    path("", v_dashboard, name="dashboard"),
    path("fingerpost/<int:pk>/", v_invoice_fingerpost, name="invoice_fingerpost"),
    
    path("list/", v_invoice_list, name="invoice_list"),
    path("create/", v_invoice_create, name="invoice_create"),
    path("update/<int:pk>/", v_invoice_update, name="invoice_update"),
    path("generate/<int:pk>/", v_invoice_generate, name="invoice_generate"),
    path("receipt/<int:pk>/", v_invoice_receipt, name="invoice_receipt"),
    path("pdf/<int:pk>/", v_invoice_pdf, name="invoice_pdf"),
    
    path("item/delete/<int:pk>/", v_invoice_item_delete, name="invoice_item_delete"),
    path("item/create/<int:fk>/<int:pk>/", v_invoice_item_create, name="invoice_item_create"),
    
    path("api/", invoiceData.as_view(), name="invoice_list_api"),
    path("item/api/", invoiceItemsData.as_view(), name="invoice_items_list_api"),
]
