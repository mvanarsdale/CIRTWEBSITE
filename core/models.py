# imports
import uuid
from django.db import models
# Used in get_absolute_url() to get URL for specified ID
from django.urls import reverse 
# allows the abillity to change django default user
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from CIRTWEBSITE import settings

# abstract user automattically includes nessary user fields 
# custom user
class CustomUser(AbstractUser):
    # custom user model fields
    name = models.CharField(max_length=150, blank=True)
  
    # roles users can have
    ROLE_CHOICES = [
        # default choice
        ('user', 'User'),
        # students
        ('author', 'Author'),
        ('viewer', 'Reviewer'),
        ('editor', 'Editor'),
        ('admin', 'Admin')
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


# base for user role groups
# skeleton provided by chatGPT
class BaseGroup(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True  # ← This makes it an abstract base class!


# model for authors
class Author(BaseGroup):
    
    class Meta:
        permissions = [ 
                       ("can_submit_PDF", "Can submit PDF"),
                       ("can_communicate", "Can communicate")
                       ]

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.user.name}"
    
# model for reviewers
class Reviewer(BaseGroup):
    
    class Meta:
        permissions = [ 
                       ("can_reviewF", "Can review"),
                       ("can_communicate", "Can communicate")
                       ]

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('reviewer-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.user.name}"

# model for reviewers
class Editor(BaseGroup):
    
    class Meta:
        permissions = [ 
                       ("can_edit", "Can edit"),
                       ("can_communicate", "Can communicate")
                       ]

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('editor-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.user.name}"


# https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django
# NOT USED IN WEBSITE
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
    author = models.ForeignKey('CustomUser', on_delete=models.RESTRICT, null=True)
    
   
    submitted_date = models.DateField(null=True, blank=True)

    # add image field for the poster PDF
    pdf = models.FileField(upload_to='papers/', null=True, blank=True)  # This saves files to MEDIA_ROOT/posters/
    
    # Use UUID for the article_number (auto-generates) from CHATGPT
    article_number = models.UUIDField(
        default=uuid.uuid4,  # Automatically generates a unique UUID
        # Makes it so it can't be manually changed)
        editable=False,  
         # Ensures each article has a unique UUID
        unique=True, 
    )

    """Four step journal publication process """
    STATUS_CHOICES = [
        # work in progress 
        ('WIP', 'WIP'),
        # submited to editor
        ('submitted', 'Submitted'),
        # editor downloaded pdf 
        ('editor_reached', 'Editor_reached'),
        # reviewer submitted comments
        ('reviewer_reached', 'Reviewer_reached'),
        # editor approves 
        ('approved', 'Approved'),
        # editor denies
        ('denied', 'Denied')
    ]
    # Role field with a dropdown
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WIP')

    # manytomany field so that the paper can have many key words and key words can have many papers
    #key_word = models.ManyToManyField(
       # KeyWord, help_text="Select a key word for this paper"
    #)
    
    def __str__(self):
        """represents model object"""
        return self.title
    
    def get_absolute_url(self):
        return reverse('paper-detail', args = [str(self.id)])
    
    #def display_key_word(self):
       # """Create a string for the keyword. 
   # This is required to display genre in Admin."""
      #  return ', '.join(key_word.name for key_word in self.key_word.all()[:3])

   # display_key_word.short_description = 'Key Word'
    

class Poster(models.Model):
    """Model representing a poster"""
    # poster title
    title = models.CharField(max_length=200)
    # foreign key - only one author , authors can have multiple papers
    # .RESCRICT keeps the paper up even if the author is deleted 
    # author of the poster 
    author = models.ForeignKey('CustomUser', on_delete=models.RESTRICT, null=True)
    
    # date 
    submitted_date = models.DateField(auto_now_add=True)
    
    # add image field for the poster PDF
    pdf = models.FileField(upload_to='posters/', null=True, blank=True)  # This saves files to MEDIA_ROOT/posters/
    
    # thumbnail for the poster 
    thumbnail = models.ImageField(upload_to='posters/thumbnails/', blank=True, null=True)
        
    def __str__(self):
        """represents model object"""
        return self.title
 
    
# code from ChatGPT - NOT USED IN WEBSITE
class Profile(models.Model):
    ROLE_CHOICES = [
        ('author', 'Author'),
        ('viewer', 'Reviewer'),
        ('editor', 'Editor'),
    ]
        
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    
# ---------MODELS FOR ADMIN PORTAL----------------
class News(models.Model):
    """Model representing a poster"""
    # news title title
    title = models.CharField(max_length=30)
    # author of the poster 
    abstract = models.CharField(max_length=100)
    
    # add image field for the news preview PDF
    pdf = models.FileField(upload_to='news/', null=True, blank=True)  # This saves files to MEDIA_ROOT/news/

        
    def __str__(self):
        """represents model object"""
        return self.title

class FAQ(models.Model):
    # question 
    question = models.CharField(max_length=100)
    # answer 
    answer = models.CharField(max_length=200)
   
    




