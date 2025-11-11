from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from .forms import ProductForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Create your views here.

def helloworld(request):
    return HttpResponse("Hello world")


def ejemploreal(request):
    context= {
        'nombre': "Audifonos gamer",
        'precio': 95000,
        'stock': 0,
    }

    return render(request, 'ejemplo.html', context)

def products(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products.html', context)

""""Vista basada en función para hacer un create"""
def create_product(request):
    pass
    # if (request.method== "GET"):
    #     form = ProductForm()
    #     return render(request, 'create_product.html', {'form': form})
    # else:
    #     form = ProductForm(request.POST)
    #     if (form.is_valid()):
    #         form.save()
    #         return redirect('invetario:products') 

"""Vistas basadas en clases (generics)"""
class ProductListView(ListView):
    model = Product
    template_name='products_generics.html'
    context_object_name='products'

    def get_queryset(self):
        return Product.objects.all()
    

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = reverse_lazy('inventario:products_generics')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = reverse_lazy('inventario:products_generics')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('inventario:products_generics')