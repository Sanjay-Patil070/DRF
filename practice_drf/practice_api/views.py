from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny


class SignupView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        # Validate required fields
        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        #  Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already taken."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        #  Create user with hashed password
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),  # important: hashes password
        )

        return Response(
            {"message": "User created successfully", "user_id": user.id},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Validate required fields
        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not check_password(password, user.password):
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Login successful",
                "user_id": user.id,
                "username": user.username,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


# Create your views here.
class EmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    security = [{"Bearer": []}]

    def get(self, request):

        employees = Employee_2.objects.all()
        serialized_data = EmployeeOutputSerializer(employees, many=True)
        print(serialized_data.data)
        return Response(serialized_data.data)


class CreateEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    security = [{"Bearer": []}]

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            Employee_2.objects.create(
                name=serializer.validated_data["name"],
                age=serializer.validated_data["age"],
                department=serializer.validated_data["department"],
                salary=serializer.validated_data["salary"],
            )
            return Response({"message": "Employee created successfully"}, status=201)
        return Response(serializer.errors, status=400)


class UpdateEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        employee_id = request.data.get("id")

        # Validate that 'id' is provided
        if not employee_id:
            return Response(
                {"error": "Employee 'id' is required in the request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            employee = Employee_2.objects.get(id=employee_id)
        except Employee_2.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)

        serializer = EmployeeSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            employee.save()
            return Response({"message": "Employee updated successfully"}, status=200)
        return Response(serializer.errors, status=400)


class DeleteEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        employee_ids = request.data.get("ids")

        if not employee_ids or not isinstance(employee_ids, list):
            return Response(
                {"error": "Please provide 'ids' as a list in the request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing_employees = Employee_2.objects.filter(id__in=employee_ids)
        existing_ids = list(existing_employees.values_list("id", flat=True))

        # Find which IDs were not found
        not_found_ids = list(set(employee_ids) - set(existing_ids))

        if not existing_employees.exists():
            return Response(
                {"error": "No matching employees found for the given IDs."},
                status=status.HTTP_404_NOT_FOUND,
            )

        deleted_count = existing_employees.count()
        existing_employees.delete()

        response = {
            "message": f"{deleted_count} employee(s) deleted successfully.",
        }

        if not_found_ids:
            response["not_found_ids"] = not_found_ids
            response["warning"] = "Some IDs were not found and were skipped."

        return Response(response, status=status.HTTP_200_OK)


class BookView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class CreateBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            Book.objects.create(
                title=serializer.validated_data["title"],
                author=serializer.validated_data["author"],
                published_date=serializer.validated_data["published_date"],
            )
            return Response({"message": "Book created successfully"}, status=201)
        return Response(serializer.errors, status=400)


class UpdateBookView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        book_id = request.data.get("id")

        # Validate that 'id' is provided
        if not book_id:
            return Response(
                {"error": "Book 'id' is required in the request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)

        serializer = BookSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            book.save()
            return Response({"message": "Book updated successfully"}, status=200)
        return Response(serializer.errors, status=400)


class DeleteBookView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        book_ids = request.data.get("ids")

        if not book_ids or not isinstance(book_ids, list):
            return Response(
                {"error": "Please provide 'ids' as a list in the request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing_books = Book.objects.filter(id__in=book_ids)
        existing_ids = list(existing_books.values_list("id", flat=True))

        # Find which IDs were not found
        not_found_ids = list(set(book_ids) - set(existing_ids))

        if not existing_books.exists():
            return Response(
                {"error": "No matching books found for the given IDs."},
                status=status.HTTP_404_NOT_FOUND,
            )

        deleted_count = existing_books.count()
        existing_books.delete()

        response = {
            "message": f"{deleted_count} book(s) deleted successfully.",
        }

        if not_found_ids:
            response["not_found_ids"] = not_found_ids
            response["warning"] = "Some IDs were not found and were skipped."

        return Response(response, status=status.HTTP_200_OK)
