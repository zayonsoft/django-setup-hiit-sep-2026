from api import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("products/", views.products, name="api_products"),
    path("products/<str:pk>/", views.ProductView.as_view(), name="api_product"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("mail/send/", views.send_user_email, name="send_user_email"),
]
