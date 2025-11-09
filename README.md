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
- Probamos yendo a la url recién creada
___
## 5. Trabajando con formularios de Django
- Debemos abrir el archivo el archivo forms.py que creamos previamente y registramos una clase form en base al modelo previamente creado

