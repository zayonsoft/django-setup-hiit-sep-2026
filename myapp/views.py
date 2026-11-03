from django.shortcuts import render, redirect
from django.http import HttpResponse
from myapp.models import Product
from .forms import ProductForm
from django.contrib import messages, auth
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    name_of_dev = "------------ZayonSoft-----------"

    list_in_class = [
        "Motunrayo",
        "Abubakar",
        "Divine",
        "Oluwatofunmi",
    ]
    context = {
        "dev": name_of_dev,
        "age": 96,
        "class_list": list_in_class,
    }

    return render(request, "home.html", context)


def about_us(request):
    return HttpResponse("<h1>About Us Page is here.....</h1>")


def take_me_to_instagram(request):
    return redirect("https://instagram.com")


def counter(request):
    context = {}
    return render(request, "counter.html", context)


def count_words(request):
    text = request.GET.get("text")

    text_count = len(text.split(" "))

    context = {
        "count": text_count,
        "text": text,
    }
    return render(request, "display_count.html", context)


def counter_post(request):
    if request.method == "POST":
        text = request.POST.get("text")
        text_count = len(text.split(" "))

        context = {
            "count": text_count,
            "text": text,
        }
        return render(request, "display_count.html", context)

    else:
        return render(request, "counter_post.html")


def products(request):
    my_products = Product.objects.all()
    context = {
        "products": my_products,
    }
    return render(request, "products.html", context)


def product(request, pk):
    chosen_product = Product.objects.get(id=pk)
    context = {
        "p": chosen_product,
    }
    return render(request, "each_product.html", context)


@login_required(login_url="signin_user")
def add_product(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.uploaded_by = request.user
            instance.save()
            return redirect("products")

    context = {
        "form": form,
    }
    return render(request, "products/add_product.html", context)


@login_required(login_url="signin_user")
def edit_product(request, pk):
    chosen = Product.objects.get(id=pk)
    if chosen.uploaded_by != request.user:
        return HttpResponse("<h1>You cannot access this page</h1>")

    form = ProductForm(instance=chosen)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=chosen, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("products")

    context = {
        "form": form,
    }
    return render(request, "products/edit_product.html", context)


@login_required(login_url="signin_user")
def delete_product(request, pk):
    prod = Product.objects.get(id=pk)

    if request.method == "POST":
        prod.delete()
        messages.success(request, "Product deleted successfully")
        return redirect("products")

    context = {
        "product": prod,
    }

    return render(request, "products/delete_product.html", context)


def create_user(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("signin_user")

    context = {"user_form": form}
    return render(request, "auth/signup.html", context)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not (username and password):
            messages.error(request, "Enter all fields")
            return redirect("signin_user")

        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid login Credentials")

    return render(request, "auth/signin.html")


def logout(request):
    auth.logout(request)
    return redirect("signin_user")
