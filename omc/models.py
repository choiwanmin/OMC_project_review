from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserIngredient(models.Model):
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.type} || {self.name}'


class Icebox(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    userIngredientId = models.ManyToManyField(UserIngredient, on_delete=models.CASCADE)
    createAt = models.DateTimeField(auto_now_add=True, verbose_name='재료추가시간')
    
    def __str__(self):
        return f'{self.userId} || {self.userIngredientId} || {self.createAt}'


class UserCustomIngredient(models.Model):
    iceBoxId = models.ForeignKey(Icebox,on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return f'{self.iceBoxId} || {self.type} || {self.name}'


class CategoryT(models.Model):
    index = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class CategoryS(models.Model):
    index = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class CategoryI(models.Model):
    index = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class CategoryM(models.Model):
    index = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    mangaeId = models.CharField(max_length=100)
    link = models.URLField()
    name = models.CharField(max_length=400)
    thumbnail = models.URLField(null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=2000)
    amount = models.CharField(null=True, blank=True, max_length=30)
    time = models.CharField(null=True, blank=True, max_length=30)
    level = models.CharField(null=True, blank=True, max_length=30)
    star = models.FloatField()
    reviewCount = models.IntegerField()
    viewCount = models.IntegerField()
    categoryTId = models.ForeignKey(CategoryT, on_delete=models.SET_NULL, null=True, blank=True)
    categorySId = models.ForeignKey(CategoryS, on_delete=models.SET_NULL, null=True, blank=True)
    categoryIId = models.ForeignKey(CategoryI, on_delete=models.SET_NULL, null=True, blank=True)
    categoryMId = models.ForeignKey(CategoryM, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=150)
    volume = models.CharField(max_length=30)
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type} || {self.name}'


class RecipeOrder(models.Model):
    number = models.IntegerField()
    description = models.CharField(max_length=2000)
    thumbnail = models.URLField(null=True, blank=True)
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipeId}-{self.number} || {self.description}'


class RecipeHashTag(models.Model):
    description = models.CharField(max_length=30)
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipeId}-{self.description}'

