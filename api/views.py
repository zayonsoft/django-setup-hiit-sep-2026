from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from myapp.models import Product
from .serializers import ProductSerializer, MailSerializer

# for class based view we'll use APIView
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.core.mail import send_mail
from django.conf import settings

# There are two types of views
# - Function based View
# - class based View

"""
@api_view(["GET"])
def products(request):
    if request.method == "GET":
        products = Product.objects.all()

        product_list = []
        for product in products:
            data = {
                "id": product.pk,
                "name": product.name,
                "description": product.description,
                "price": product.price,
            }

            product_list.append(data)

        return Response(product_list)

"""


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def products(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        request_data = request.data
        request_data["uploaded_by"] = request.user.id
        serializer = ProductSerializer(data=request_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({"detail": "Product added successfully"})


class ProductView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def patch(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({"detail": "product has been updated"})

    def put(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({"detail": "product updated"})

    def delete(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response({"detail": "Product deleted!"})


@api_view(["POST"])
def send_user_email(request):
    serializer = MailSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        subject = serializer.validated_data.get("subject")  # type: ignore
        body = serializer.validated_data.get("body")  # type: ignore
        receiver = serializer.validated_data.get("receiver")  # type: ignore

        send_mail(
            subject=str(subject),
            message=str(body),
            from_email=f"Zayonsoft Hiit Plc<{settings.DEFAULT_FROM_EMAIL}>",
            recipient_list=[str(receiver)],
        )

        return Response({"detail": "Mail Sent successfully"})
