from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid, os
from pytz import timezone
import datetime

# Create your models here.

class UserManager(BaseUserManager):
    
    use_in_migrations = True    
   
    def create_user(self, email, nickname, password):

        if not email:            
            raise ValueError('must have user email')
        if not password:            
            raise ValueError('must have user password')

        user = self.model(            
            email=self.normalize_email(email),
            nickname=nickname              
        )        
        user.set_password(password)        
        user.save(using=self._db)        
        return user

    def create_superuser(self, email, nickname, password):

        user = self.create_user(            
            email = self.normalize_email(email),
            nickname=nickname,                       
            password=password        
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user 


class User(AbstractBaseUser, PermissionsMixin):
    
    objects = UserManager()
    
    email = models.EmailField(        
        max_length=255,        
        unique=True,    
    )
    nickname = models.CharField(
        u'닉네임', 
        max_length=10, 
        blank=False, 
        unique=True, 
        default=''
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='image/avatar/',
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    CHOICE_GENDER=((None, ""), (True, "남자"), (False,"여자"))
    gender = models.BooleanField(blank=False, default=None, choices=CHOICE_GENDER, verbose_name='gender')
    CHOICE_AGEGROUP = (('10', '10~19세'), ('20', '20~29세'), ('30', '30~39세'), ('40', '40~49세'), ('50', '50~59세'), ('60', '60~69세'), ('70', '70~79세'), ('80', '80~89세'), ('90', '90~99세'),)
    ageGroup = models.CharField(max_length=2, choices=CHOICE_AGEGROUP, verbose_name='age_group')
    CHOICE_HOUSEHOLDSIZE = (('1', '1인 가구'), ('2', '2인 가구'), ('3', '3인 가구'), ('4', '4인 가구'), ('5', '5인 가구'), ('6', '6인 가구'), ('7', '7인 가구'), ('8', '8인 가구'), ('9', '9인 가구'), ('10', '10인 가구 이상'),)
    householdSize = models.CharField(max_length=3, choices=CHOICE_HOUSEHOLDSIZE, verbose_name='household_size')

    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['nickname']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# class User(AbstractUser):
#     CHOICE_GENDER=((0, ""), (1, "남자"), (2,"여자"))
#     gender = models.BooleanField(blank=False, default=0, choices=CHOICE_GENDER, verbose_name='gender')
#     CHOICE_AGEGROUP = (('10', '10~19세'), ('20', '20~29세'), ('30', '30~39세'), ('40', '40~49세'), ('50', '50~59세'), ('60', '60~69세'), ('70', '70~79세'), ('80', '80~89세'), ('90', '90~99세'),)
#     ageGroup = models.CharField(max_length=2, choices=CHOICE_AGEGROUP, verbose_name='age_group')
#     CHOICE_HOUSEHOLDSIZE = (('1', '1인 가구'), ('2', '2인 가구'), ('3', '3인 가구'), ('4', '4인 가구'), ('5', '5인 가구'), ('6', '6인 가구'), ('7', '7인 가구'), ('8', '8인 가구'), ('9', '9인 가구'), ('10', '10인 가구 이상'),)
#     householdSize = models.CharField(max_length=3, choices=CHOICE_HOUSEHOLDSIZE, verbose_name='household_size')


class UserIngredient(models.Model):
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.type} || {self.name}'


class Icebox(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    userIngredientId = models.ManyToManyField(UserIngredient, blank=True, related_name='userIngredient_iceboxes')
    
    def __str__(self):
        return f'{self.userId} || {self.userIngredientId} || {self.createAt}'


class UserCustomIngredient(models.Model):
    iceBoxId = models.ForeignKey(Icebox,on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='재료추가시간')
    name = models.CharField(max_length=30)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    
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
    like = models.ManyToManyField(User, related_name='like_recipes', blank=True)
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


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    today = datetime.datetime.now(timezone('Asia/Seoul'))
    year = today.strftime('%Y')
    month = today.strftime('%m')
    day = today.strftime('%d')
    return os.path.join(f'media/{year}/{month}/{day}/', filename)

class Comment(models.Model):
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='댓글생성시간')
    modifiedAt = models.DateTimeField(auto_now=True, verbose_name='댓글수정시간')
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.IntegerField()
    thumbnail = models.ImageField(null=True, blank=True, upload_to=get_file_path)

    def get_absolute_url(self):
        return f'{self.recipeId.get_absolute_url()}#comment-{self.pk}'

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