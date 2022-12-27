from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    CHOICE_GENDER=((0, ""), (1, "남자"), (2,"여자"))
    gender = models.BooleanField(blank=False, default=0, choices=CHOICE_GENDER, verbose_name='gender')
    CHOICE_AGEGROUP = (('10', '10~19세'), ('20', '20~29세'), ('30', '30~39세'), ('40', '40~49세'), ('50', '50~59세'), ('60', '60~69세'), ('70', '70~79세'), ('80', '80~89세'), ('90', '90~99세'),)
    ageGroup = models.CharField(max_length=2, choices=CHOICE_AGEGROUP, verbose_name='age_group')
    CHOICE_HOUSEHOLDSIZE = (('1', '1인 가구'), ('2', '2인 가구'), ('3', '3인 가구'), ('4', '4인 가구'), ('5', '5인 가구'), ('6', '6인 가구'), ('7', '7인 가구'), ('8', '8인 가구'), ('9', '9인 가구'), ('10', '10인 가구 이상'),)
    householdSize = models.CharField(max_length=3, choices=CHOICE_HOUSEHOLDSIZE, verbose_name='household_size')


class UserIngredient(models.Model):
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.type} || {self.name}'


class Icebox(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    userIngredientId = models.ManyToManyField(UserIngredient, blank=True)
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

    def get_absolute_url(self):
        return f'/recipe/{self.pk}'


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
    description = models.SlugField(max_length=30, allow_unicode=True)
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipeId}-{self.description}'
    
    def get_absolute_url(self):
        return f'/recipe/tag/{self.slug}/'

    class Meta:
        verbose_name_plural = 'RecipeHashTags'