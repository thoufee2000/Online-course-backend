from rest_framework import serializers
from . models import State,City,Course_category,Course


class Stateview(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"

class Cityview(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

class CategoryView(serializers.ModelSerializer):
    class Meta:
        model=Course_category
        fields="__all__"

class SearchView(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields="__all__"