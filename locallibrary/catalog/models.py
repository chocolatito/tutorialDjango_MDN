from django.db import models
# Usado para generar URLs invirtiendo los patrones de URL
from django.urls import reverse
# Requerida para las instancias de libros únicos
import uuid
from datetime import date
# Requerido para asignar al usuario como prestatario (borrower)
from django.contrib.auth.models import User


#  _______________________________
# | AQUÍ COMIENZA UN NUEVO MODELO |

class Genre(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


#  _______________________________
# | AQUÍ COMIENZA UN NUEVO MODELO |

class Language(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


#  _______________________________
# | AQUÍ COMIENZA UN NUEVO MODELO |

class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    isbn = models.CharField('ISBN', max_length=13)
    genre = models.ManyToManyField(Genre)

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


#  _______________________________
# | AQUÍ COMIENZA UN NUEVO MODELO |

class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1,
                              choices=LOAN_STATUS,
                              blank=True,
                              default='m')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)


#  _______________________________
# | AQUÍ COMIENZA UN NUEVO MODELO |

class Author(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)
