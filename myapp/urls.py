from django.urls import path
from myapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about_us, name="about"),
    path("instagram", views.take_me_to_instagram),
    path("counter", views.counter, name="counter"),
    path("counter/post", views.counter_post, name="counter_post"),
    path("counter/result", views.count_words, name="count_result"),
    path("products", views.products, name="products"),
    path("products/<str:pk>", views.product, name="product"),
    path("add_product", views.add_product, name="add_product"),
    path("products/edit/<str:pk>", views.edit_product, name="edit_product"),
    path("products/delete/<str:pk>", views.delete_product, name="delete_product"),
    path("auth/signup", views.create_user, name="create_user"),
    path("auth/signin", views.login, name="signin_user"),
    path("auth/logout", views.logout, name="logout"),
]
