from django.db import models

# Used in get_absolute_url() to get URL for specified ID
from django.urls import reverse 

from django.contrib.auth.models import AbstractUser

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
        
        