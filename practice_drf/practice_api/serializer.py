from rest_framework import serializers


class EmployeeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    age = serializers.CharField(max_length=100)
    department = serializers.CharField(max_length=100)
    salary = serializers.FloatField()

    class Meta:
        # fields = "__all__"
        model = "Employee_2"


class EmployeeOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    age = serializers.CharField(max_length=100)
    department = serializers.CharField(max_length=100)
    salary = serializers.FloatField()

    class Meta:
        # fields = "__all__"
        model = "Employee_2"


class BookSerializer(serializers.Serializer):
    # id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=100)
    published_date = serializers.DateField()

    class Meta:
        model = "Book"
        # fields = "__all__"
