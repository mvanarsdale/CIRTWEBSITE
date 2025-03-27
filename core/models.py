
import uuid
from django.db import models

# Used in get_absolute_url() to get URL for specified ID
from django.urls import reverse 

from django.contrib.auth.models import AbstractUser

from django.db.models import UniqueConstraint
from django.db.models.functions import Lower


#from core import admin

# abstract user automattically includes nessary user fields 
class CustomUser(AbstractUser):
    # Your custom user model fields
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=150, blank=True)
    
    
    # roles
    ROLE_CHOICES = [
        ('user', 'User'),
        ('author', 'Author'),
        ('viewer', 'Reviewer'),
        ('editor', 'Editor'),
    ]
    # Role field with a dropdown
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    
    groups = models.ManyToManyField(
        'auth.Group', 
        blank=True, 
        related_name='core_user_set'  # Specify a unique related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        blank=True, 
        related_name='core_user_permissions'  # Specify a unique related_name
    )

class Role(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
 

class Author(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='author_profile', default=1)
    

    class Meta:
        permissions = [ 
                       ("can_submit_PDF", "Can submit PDF"),
                       ("can_communicate", "Can communicate")
                       ]

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f"Author Profile: {self.user.username}"


 
# https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django
class KeyWord(models.Model):
    """Model that represents the keywords class"""
    # using the char field 
    name = models.CharField(
        max_length=200,
        # only one of that key word can exists 
        unique = True,
        help_text = "Enter key words"
    )


    def __str__(self):
        """String for representing the Model object"""
        return self.name
    
    def get_absolute_url(self):
        """returns the url to acess a keyword instance"""
        return reverse('key_word-detail', args=[str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
    
    name='key_word_name_case_insensitive_unique', 
    # error shown when user tries to create keyword that already exists
    violation_error_message = "Key word already exists (case insensitive match)"
        ),
        ]

      
# https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django
class Paper(models.Model):
    """Model representing a paper"""
    title = models.CharField(max_length=200)
    # foreign key - only one author , authors can have multiple papers
    # .RESCRICT keeps the paper up even if the author is deleted 
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the paper")
    submitted_date = models.DateField(null=True, blank=True)
    
    
    # Use UUID for the article_number (auto-generates) from CHATGPT
    article_number = models.UUIDField(
        default=uuid.uuid4,  # Automatically generates a unique UUID
        # Makes it so it can't be manually changed)
        editable=False,  
         # Ensures each article has a unique UUID
        unique=True, 
    )
    
    # manytomany field so that the paper can have many key words and key words can have many papers
    key_word = models.ManyToManyField(
        KeyWord, help_text="Select a key word for this paper"
    )
    
    def __str__(self):
        """represents model object"""
        return self.title
    
    def get_absolute_url(self):
        return reverse('paper-detail', args = [str(self.id)])
    
    def display_key_word(self):
        """Create a string for the Genre. 
    This is required to display genre in Admin."""
        return ', '.join(key_word.name for key_word in self.key_word.all()[:3])

    display_key_word.short_description = 'Key Word'
    

class Poster(models.Model):
    """Model representing a paper"""
    title = models.CharField(max_length=200)
    # foreign key - only one author , authors can have multiple papers
    # .RESCRICT keeps the paper up even if the author is deleted 
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    
    # add image field for the poster PDF
    
    submitted_date = models.DateField(null=True, blank=True)
    
# code from ChatGPT
class Profile(models.Model):
    ROLE_CHOICES = [
        ('author', 'Author'),
        ('viewer', 'Reviewer'),
        ('editor', 'Editor'),
    ]
        
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
   
    
    
    

    
    




