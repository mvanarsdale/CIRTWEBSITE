from django.db import models

# Used in get_absolute_url() to get URL for specified ID
from django.urls import reverse 

"""Roles"""
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


class Reviewer(models.Model):
    """Model representing a reviewer."""
    class Meta:
        permissions = [
            # can see draft requests 
            ("can_mark_reviewing", "Can mark papers as reviewing"),
            ("can_mark_reviewed_Accept", "Can mark papers as accepted"),
            ("can_mark_reviewed_Denied", "Can mark papers as denied"),
            
            
        ]

class Editor(Reviewer):
    """Model representing an editor."""
    class Meta:
        proxy = True
        permissions = [
            # can see accepected drafts 
            ("can_mark_editing", "Can mark papers as editing"),
            ("can_mark_edited", "Can mark papers as edited"),
            
            ("can_submit_comments_to_the_author", "Can submit comments to the author"),
            ("can_submit_comments_to_the_author_and_reviewer", "Can submit comments to the author and reviewer")
        ]
        
        