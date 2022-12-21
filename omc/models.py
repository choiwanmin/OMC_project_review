from django.db import models

# Create your models here.
class CategoryT(models.Model):
    index = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'cat T || {self.name}'


class CategoryS(models.Model):
    index = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'cat S || {self.name}'


class CategoryI(models.Model):
    index = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'cat I || {self.name}'


class CategoryM(models.Model):
    index = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'catM || {self.name}'


class Recipe(models.Model):
    mangaeId = models.CharField(max_length=100)
    link = models.URLField()
    name = models.CharField(max_length=200)
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
        return f'recipe || {self.name}'


class Ingredient(models.Model):
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    volume = models.CharField(max_length=30)
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'ingredient || {self.type} || {self.name}'


class RecipeOrder(models.Model):
    number = models.IntegerField()
    description = models.URLField()
    thumbnail = models.URLField(null=True, blank=True)
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'order{self.recipeId}-{self.number} || {self.description}'


class RecipeHashTag(models.Model):
    description = models.CharField(max_length=30)
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'hashTag || {self.recipeId}-{self.description}'

