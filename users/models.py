import uuid
from django.db import models

# Used in get_absolute_url() to get URL for specified ID
from django.urls import reverse 

from django.contrib.auth.models import AbstractUser

#from core import admin

# abstract user automattically includes nessary user fields 
class User(AbstractUser):
    """A typical class defining a model, derived from the Model class."""
    #profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)
    # roles user can have 
    role = models.ManyToManyField('Role', related_name='users', blank=True)
    
    # code fronm chatGPT
    def __str__(self):
        # displays username and roles
        return f"{self.username} ({', '.join([role.name for role in self.role.all()]) or 'No Roles'})"

    # code from chatGPT
    def get_absolute_url(self):
        # create url for users profile page
        return reverse('user_profile', kwargs={'username': self.username})
    
    class Meta:
        permissions = [
            ("can_access_dash", "Can access dashboard"),
        ]

class Role(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_profile', default=1)
    

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


class Reviewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reviewer_profile', default=1)
    """Model representing a reviewer."""
    class Meta:
        permissions = [
            # can see draft requests 
            ("can_mark_reviewing", "Can mark papers as reviewing"),
            ("can_mark_reviewed_Accept", "Can mark papers as accepted"),
            ("can_mark_reviewed_Denied", "Can mark papers as denied"),  
            
        ]
    def __str__(self):
        return f"Reviewer Profile: {self.user.username}"

class Editor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='editor_profile', default=1)
    """Model representing an editor."""
    class Meta:
        permissions = [
            # can see accepected drafts 
            ("can_mark_editing", "Can mark papers as editing"),
            ("can_mark_edited", "Can mark papers as edited"),
            
            ("can_submit_comments_to_the_author", "Can submit comments to the author"),
            ("can_submit_comments_to_the_author_and_reviewer", "Can submit comments to the author and reviewer")
        ]
        
    def __str__(self):
        return f"Editor Profile: {self.user.username}"
    
    
    
## paper, paper progress, and something else I forgot
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

    
# from ChatGPT 
class PaperProgress(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('revision', 'Revisions Needed'),
        ('accepted', 'Accepted'),            
        ('published', 'Published'),
    ]
    
    # one toomany field assures one one progress bar for each paper
    # foreign key to get information from paper class
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)  # Links to a single paper
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    last_updated = models.DateTimeField(auto_now=True)  # Auto-updates whenever the status changes


    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    def __str__(self):
        return f"{self.paper.title} - {self.get_status_display()}"
    
         
# https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    #date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = [ 
                       ("can_submit_PDF", "Can submit PDF"),
                       ("can_communicate", "Can communicate")
                       ]

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
        
        