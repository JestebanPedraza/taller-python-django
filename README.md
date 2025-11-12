# Mini curso práctico de Django
Introducción al desarrollo web con Python y Django. Este repositorio contiene el codigo final que se espera desarrollar durante el minicurso-taller de django, en el cual se presentan conceptos como: arquitectura de django, rutas, templates, ORM de django, formularios, tipos de vistas, etc.
___
## 1. Primeros pasos - Configurar el entorno de trabajo
- Crear una carpeta con el nombre del proyecto
> [!IMPORTANT]
> Siempre trabajar cada proyecto con entorno virtual
- Dentro de la carpeta creamos el entorno virtual: `python -m venv venv`
- Instalar django: `pip install django`
> [!NOTE]
> Para ver las librerias instaladas en el entorno virtual: `pip list`
___
## 2. Iniciar proyecto de Django
- Para crear un proyecto de django debemos escribir en la terminal: `django-admin startproject myfirstproject .`
- Ejecutar servidor: `python manage.py runserver`
- Creando super usuario para acceder al panel de administración:
  - Primero se debe hacer migraciones: `python manage.py makemigrations` y luego `python manage.py migrate`
  - Crear super usuario: `python manage.py createsuperuser`
  - Acceder al panel de admin: Debemos ejecutar el servidor y colocar '/admin' en la url
___
## 3. Creando nuestra primera aplicación
- Para crear una aplicación en django se utiliza el comando: `python manage.py startapp inventario`
- Vamos a crear dos archivos python muy importantes en la carpeta de la aplicación que acabamos de crear:
  - forms.py y urls.py
> [!IMPORTANT]
> Debemos establecer un path de rutas para evitar sobrecargar el urls de la carpeta de proyecto y que cada app tenga su propio path de rutas

- Abrimos el archivo urls.py recién creado en la app inventario y agregamos el urlpatterns: 
```
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path(),
]
```
- Despues tenemos que incluir las rutas de esta aplicación al archivo de urls de rutas del proyecto. Entonces vamos al urls.py de myfirstproject y agregamos lo siguiente:
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventario.urls'))
]
```
- Ahora abrimos el views.py de la aplicacion inventario y creamos la siguiente función:
```
def helloworld(request):
    return HttpResponse("Hola mundo!")
```
Esto no tendrá ningun efecto aún por que no hemos definido la url que ejecutará esta función, por ende volvemos al archivo urls.py de la app y agregamos lo siguiente dentro del urlpatterns:
```
    path('inventario', views.helloworld),
```
- Testeamos lo que hemos hecho ejecutando el servidor y agregando inventario a la url: 'http://127.0.0.1:8000/inventario'
___
### 3.1 Utilizando el motor de plantillas de Django
- Vamos al views.py de la app inventario y creamos la siguiente función:
```
def ejemploreal(request):
    context= {
        'nombre': "Audifonos gamer",
        'precio': 95000,
        'stock': 5,
    }

    return render(request, 'ejemplo.html', context)
```
- Dentro de la carpeta inventario debemos crear una carpeta llamada 'templates' y dentro de templates creamos el archivo `ejemplo.html`
A este archivo podemos agregarle todo el contenido html que querramos:
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ejemplo de Template</title>
</head>
<body>
    <h1>Mi pimera template en django</h1>
    <h3>Información enviada desde la view:</h3>
</body>
</html>
```
- Debemos configurar la ruta para esta nueva view, entonces vamos a urls.py de la app inventario y agregamos un nuevo path: `path('inventario/ejemplo', views.ejemploreal),`
- Ejecutamos nuevamente el servidor y probamos la nueva ruta  `http://127.0.0.1:8000/inventario/ejemplo`
- Posiblemente no se cargue la template, y es porque cada aplicación que creamos debe estar registrada en el settings.py de la carpeta del principal del proyecto:
```
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventario',
]
...
```
___

## 4. Trabajando con los modelos de datos
Hasta el momento no hemos creado ningun modelo por ende no podemos crear formularios para realizar operaciones CRUD. Por ende vamos a comezar primero por construir el modelo de productos.
- Vamos a el archivo models.py de la app inventario. Los modelos en Django se escriben con sintaxis de clases, es decir POO, por ende el modelo que vamos a construir debe quedar así:
```
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```
- Después de guardar, debemos ejecutar nuevamente las migraciones (se debe hacer cada vez que aregamos, actualizamos o borramos un modelo)
- Ahora esperamos que ingresando al admin de django veamos este nuevo modelo y podamos agregar y ver productos sin embargo, debemos hacar una pequeña configuración:
  - Vamos al admin.py de la app inventario y registramos nuestro modelo en el objeto admin:
```
from django.contrib import admin

from .models import Product
# Register your models here.

admin.site.register(Product)
```
Ahora si, podemos ingresar al admin y realizar operaciones en el modelo. Agregamos algunos  productos.
- Crearemos una vista para mostrar los productos que hemos registrado en la base de datos
  - Importamos nuestro modelo en el archivo views.py; `from models import Product`
  - Ahora creamos nuestra función y dentro vamos a utilizar al ORM de Django para realizar una query a la base de datos
  - Agregamos la información de nuestra consulta en la variable context
  - Creamos una template para que renderice la información de nuestra vista

views.py:
```
def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products.html', context)
```
En la template products.html:
```
<body>
    <h2>Lista de productos</h2>
    {% for product in products %}
        <h3>{{ product.name }}</h3>
        <p>{{ product.description }}<p>
        <b>{{ product.price }}</b>
        <hr>
        <br>
    {% endfor %}
</body>
```
- Agregamos el path de la url de la nueva vista en archivo urls.py: `.. path('inventario/products', views.products), ...`
- Probamos la url recién creada
___
## 5. Trabajando con formularios de Django
- Primero que todo vamos a modificar el urls.py, debemos asignar un nombre a cada url para facilitar el uso de direcciones en django:
```
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('inventario', views.helloworld, name="hello"),
    path('inventario/ejemplo', views.ejemploreal, name="ejemplo"),
    path('inventario/products', views.products, name="products"),
]
```
- Luego, debemos abrir el archivo el archivo forms.py que creamos previamente y registramos una clase form en base al modelo previamente creado y registrar nuestro primer formulario del modelo:
```
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """Formulario para el modelo Product."""

    class Meta:
        model = Product
        fields = '__all__'
 
```
- Creamos una nueva template para crear el formulario: `create_product.html` y creamos el html de la página:
```
<body>
    <h2>Crear un producto</h2>
    <form action="" method="post">
        {% csrf_token %}
        {{form.as_p}}
        <input type="submit" value="Enviar">
    </form>
</body>
```
- Creamos la vista en el views.py:
```
def create_product(request):
    if (request.method== "GET"):
        form = ProductForm()
        return render(request, 'create_product.html', {'form': form})
    else:
        form = ProductForm(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect('invetario:products') 
```
- Registramos esta nueva función en el urls.py: `...path('inventario/create_product', views.create_product, name="create_product"),...`
- Actualizamos nuestra página de productos para agregar un link que nos permita ir a la página de crear producto:
```
<body>
    <h2>Lista de productos</h2>
    <a href="{% url 'inventario:create_product' %}">Crear un producto</a>
    <div>
        {% for product in products %}
            <h3>{{ product.name }}</h3>
            <p>{{ product.description }}<p>
            <b>{{ product.price }}</b>
            <hr>
            <br>
        {% endfor %}
    </div>
</body>
```
- Probamos creando un nuevo producto.
___
## 6. Vistas basadas en funciones VS Vistas basadas en clases(vista genérica)
Estaremos explorando las clases genéricas de django y haremos el CRUD completo con ellas para ver lo mucho que nos simplifica.
- Importamos las librerías necesarias para llamar a los generics: `from django.views.generic import ListView, CreateView, UpdateView, DeleteView` y a `
from django.urls import reverse_lazy` que lo utilizaremos dentro de las generics para redireccionar
- Creamos una template nueva para listar productos con la clase genérica: `products_generics.html`
```
<body>
    <h2>Lista de productos</h2>
    <div>
        {% for product in products %}
            <h3>{{ product.name }}</h3>
            <p>{{ product.description }}<p>
            <b>{{ product.price }}</b>
        {% endfor %}
            
    </div>
</body>
```
- Creamos una clase para listar los productosy vinculamos la template recién creada:
```
class ProductListView(ListView):
    model = Product
    template_name='products_generics.html'
    context_object_name='products'

    def get_queryset(self):
        return Product.objects.all()
```
- Vamos al urls.py y definimos la nueva ruta para acceder a la vista genérica de listar productos: `path('inventario/products-generics', views.ProductListView.as_view(), name="products_generics"),`
- Probamos accediendo a a dirección `http://127.0.0.1:8000/inventario/products-generics`
> [!NOTE]
> Podemos reutilizar la template del formulario de create para las siguientes vistas create y update
- Vamos a crear las vistas Create y Update, ellas estarán relacionadas con la misma template, ya que necesitan el mismo formulario
```
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
```
- Vamos al urls.py y definimos la ruta para crear un producto:
```
...
path('inventario/create-products-generics', views.ProductCreateView.as_view(), name="create_products_generics"),
...
```
- Agregamos un botón para crear un producto en la página de productos:
```
...
<body>
    <h2>Lista de productos</h2>
    <a href="{% url 'inventario:create_products_generics' %}">Crear un producto</a>
...
```
- Probamos creando un producto.
- Ahora vamos a definir la ruta para Editar un producto:
> [!IMPORTANT]
> Para editar un producto debemos pasar el ID del producto como parámetro para que la base de datos identifique el producto que se quiere editar y se carguen los datos del mismo.
Por suerte Django nos permite enviar estos valores mediante la url agregando `/<int:pk>` donde lo que va antes de los dos puntos el el tipo de dato, y después de los dos puntos el nombre de la variable. Pero ¿y como enviamos esa variable?
- Primero dejemos listas las nuevas urls:
```
...
path('inventario/create-products-generics', views.ProductCreateView.as_view(), name="create_products_generics"),
path('inventario/update-products-generics/<int:pk>', views.ProductUpdateView.as_view(), name="update_products_generics"),
...
```
- Ahora si, creemos un botón para Editar el producto:
```
...
<b>{{ product.price }}</b>
<a href="{% url 'inventario:update_products_generics' pk=product.id %}">Editar</a>
...
```
El ID del producto se lo enviamos mediante la url. El nombre de la variable debe ser igual al que definimos en la url del path
- Listo, probamos dando clic en el botón Editar
Ahora solo falta crear la vista para eliminar un producto.
- Creamos la vista:
```
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('inventario:products_generics')
```
Ahora, las vista genérica Delete siempre va pedir cargar una template o un modal con un formulario para confirmar la eliminación. Por ende, crearemos una nueva template.
- Creamos la template: `product_confirm_delete.html` y dentro escribimos algo así:
```
<h2>¿Seguro que quieres eliminar este producto?</h2>
<p><strong>{{ product.name }}</strong></p>

<form method="post">
    {% csrf_token %}
    <button type="submit">Sí, eliminar</button>
    <a href="{% url 'inventario:products_generics' %}">Cancelar</a>
</form>
```
- Por último, agregamos un botón para poder eliminar un producto en la página donde mostramos cada producto
```
...
<b>{{ product.price }}</b>
<a href="{% url 'inventario:update_products_generics' pk=product.id %}">Editar</a>
<a href="{% url 'inventario:delete_products_generics' pk=product.id %}">Eliminar</a>
...
```
---
## ✨ ¡Felicidades! ✨
Has terminado tu primera aplicación en Django y haz realizado todas las operaciones de un CRUD 👏
---
___
> [!NOTE]
>  **¡BONUS! Agregando estilos con bootstrap**

Podemos agregar bootstrap a nuestra app de forma sencilla usando la CDN de bootstrap, para ello debemos definir un layout y que cargue el contenido html que se debe repetir en todas las templates y extender este layout a todas las demas templates.
- Creamos el layout: `templates/layout.html`
- Agregamos el contenido html, la CDN de bootstrap y los bloques para incrustar el contenido de otras templates 
[Dando clic aquí](https://gist.github.com/JestebanPedraza/41490db7ce9dd18ea9cb19efdf11e4c0)
- Ahora agregaremos estilos a nuestras templates de listar productos y los formularios:
Template para listar productos:
[Dando clic aquí](https://gist.github.com/JestebanPedraza/5933136ed400de136a509e895cedd18d)
Template Formulario:
```
{% extends 'layout.html' %} {% block title %}Sistema POS{% endblock %}
{% block content %}
    <h2 class="m-4 text-center">Formulario de producto producto</h2>

    <form action="" method="post" class="w-50 mx-auto border rounded p-4 shadow-sm bg-light">
        {% csrf_token %}
        <div class="mb-3">
            {{ form.as_p }}
        </div>
        <div class="text-center">
            <button type="submit" class="btn btn-primary">Enviar</button>
        </div>
    </form>
{% endblock %}
```
Sin embargo debemos aplicar estilos a los campos del formulario, pero como este form se genera dinámicamente con la clase genérica tenemos que agregar las clases en el formulario del modelo
- Vamos a forms.py y agregamos lo siguiente:
```
...
class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción (opcional)'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio en USD'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad disponible'
            }),
            'available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
```
---
## ✨ ¡Felicidades! ✨
Lograste aprender a añadir estilos de bootstrap a tu aplicación con Django 👏
---
