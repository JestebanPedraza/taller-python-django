from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('inventario', views.helloworld, name="hello"),
    path('inventario/ejemplo', views.ejemploreal, name="ejemplo"),
    path('inventario/products', views.products, name="products"),
    path('inventario/create-product', views.create_product, name="create_product"),
    #Vistas genéricas
    path('inventario/products-generics', views.ProductListView.as_view(), name="products_generics"),
    path('inventario/create-products-generics', views.ProductCreateView.as_view(), name="create_products_generics"),
    path('inventario/update-products-generics/<int:pk>', views.ProductUpdateView.as_view(), name="update_products_generics"),
    path('inventario/delete-products-generics/<int:pk>', views.ProductDeleteView.as_view(), name="delete_products_generics"),
]