from django.urls import path
from orders import views

urlpatterns = [
    path('customerOrders/<int:customer>',
         views.CustomerViewOrders.as_view(),
         name='customer-orders'),
    path('customers',
         views.CustomersViewAll.as_view(),
         name='customers'),
]
