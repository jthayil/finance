"""
path('', views.home, name='home')
path('', Home.as_view(), name='home')
path('blog/', include('blog.urls'))
"""

from django.urls import path
from masters.views import inventoryData, pincodeData, v_company_create, v_company_edit, v_company_list, v_hsn_create, v_hsn_edit, v_hsn_list, v_inventory_create, v_inventory_edit, v_inventory_list, v_pincode_create, v_pincode_list, v_user_list, v_user_create, v_user_edit, v_inventory_template, v_inventory_import

app_name = "masters"


urlpatterns = [
    # path("import/", v_import_masters, name="import_masters"),

    path("inventory/", v_inventory_list, name="inventory_list"),
    path("inventory/create/", v_inventory_create, name="inventory_create"),
    path("inventory/edit/<int:pk>/", v_inventory_edit, name="inventory_edit"),
    path("inventory/template/", v_inventory_template, name="inventory_template"),
    path("inventory/import/", v_inventory_import, name="inventory_import"),
    path("inventory/api/", inventoryData.as_view(), name="inventory_list_api"),


    path("user/", v_user_list, name="user_list"),
    path("user/create/", v_user_create, name="user_create"),
    path("user/edit/<int:pk>/", v_user_edit, name="user_edit"),
    
    path("company/", v_company_list, name="company_list"),
    path("company/create/", v_company_create, name="company_create"),
    path("company/edit/<int:pk>/", v_company_edit, name="company_edit"),

    path("pincode/", v_pincode_list, name="pincode_list"),
    path("pincode/create/", v_pincode_create, name="pincode_create"),
    path("pincode/api/", pincodeData.as_view(), name="pincode_list_api"),

    path("hsn/", v_hsn_list, name="hsn_list"),
    path("hsn/create/", v_hsn_create, name="hsn_create"),
    path("hsn/edit/<int:pk>/", v_hsn_edit, name="hsn_edit"),
]


# eof
