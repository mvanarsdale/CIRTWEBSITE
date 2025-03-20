from django.db import models

# Used in get_absolute_url() to get URL for specified ID
from django.urls import reverse 

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field

# django import that generates an ID number for each paper
import uuid

# code refrenced from: https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django
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

    
# code refrenced from: https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django
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
    
    
# code from: ChatGPT 
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
    
         
