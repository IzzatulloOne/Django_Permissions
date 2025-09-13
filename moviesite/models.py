from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import magic

def limit_video(value):
    limit = 2 * 1024 * 1024 * 1024
    if value.size > limit:
        raise ValueError("Файл слишком большой. Максимум 2 ГБ ❌. / Faylni razmeri juda kotta maksimum 2GB ❌.")

def check_mime(file):
    mime = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    if mime in ['videos/mp4', 'videos/mov', 'videos/amv','videos/mkv','videos/avi']:
        pass
    else:
        raise ValidationError('Недопустимый тип файла ❌./ Bu fayl sistemaga togri kemaydi ❌.')

class Genre(models.Model):
    type = models.CharField(verbose_name="Nomi", max_length=50)

    def __str__(self):
        return self.type

    class Meta: 
        ordering = ['type']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        db_table = 'genres'

class Movie(models.Model):
    title = models.CharField(verbose_name="Nomi", max_length=75, unique=True)
    director = models.CharField(verbose_name="Rejissori", max_length=100, null=True, blank=True)
    description = models.TextField(verbose_name="Ma'lumoti", null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies', verbose_name="Janri")
    cover = models.ImageField(verbose_name="Posteri", upload_to='covers/', null=True, blank=True)
    video = models.FileField(verbose_name="Kinosi", 
                            upload_to='videos/',  
                            null=True, blank=True, 
                            validators=[
                                FileExtensionValidator(['mp4','mpg', 'mov', 'amv','mkv','avi']),
                                limit_video,
                                check_mime
                            ]
                        )
    release = models.DateField(verbose_name="Chiqgan sanasi")
    views = models.IntegerField(verbose_name="Ko'rishlar soni", default=0)
    published = models.BooleanField(verbose_name="Saytga chiqarish?", default=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [
            ('publish_movie', "Can publish movie")
        ]
        ordering = ['-release']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        db_table = 'movies'

class Comment(models.Model):
    text = models.CharField(verbose_name="Matni", max_length=500)
    movie  = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Kino")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        db_table = 'comments'

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_photo')
    phone = models.CharField(max_length=13, unique=True)
    job = models.CharField(max_length=120)
    website = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=160)
    bio = models.CharField(max_length=350)
    twitter = models.CharField(max_length=90, unique=True, null=True, blank=True)
    facebook = models.CharField(max_length=90, unique=True, null=True, blank=True)
    telegram = models.CharField(max_length=90, unique=True, null=True, blank=True)
    linkedin = models.CharField(max_length=90, unique=True, null=True, blank=True)

    def __str__(self):
        return self.user.username