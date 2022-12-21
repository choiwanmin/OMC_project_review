from django.db import models

# Create your models here.
class CategoryT(models.Model):
    index = models.IntegerField()
    name = models.CharField(max_length=30)


class CategoryS(models.Model):
    index = models.IntegerField()
    name = models.CharField(max_length=30)


class CategoryI(models.Model):
    index = models.IntegerField()
    name = models.CharField(max_length=30)


class CategoryM(models.Model):
    index = models.IntegerField()
    name = models.CharField(max_length=30)


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


class Ingredient(models.Model):
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    volume = models.CharField(max_length=30)
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class RecipeOrder(models.Model):
    number = models.IntegerField()
    description = models.URLField()
    thumbnail = models.URLField(null=True, blank=True)
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class RecipeHashTag(models.Model):
    description = models.CharField(max_length=30)
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)


