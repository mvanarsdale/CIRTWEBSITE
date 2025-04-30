import os
from pdf2image import convert_from_path
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Poster

@receiver(post_save, sender=Poster)
def generate_pdf_thumbnail(sender, instance, created, **kwargs):
    if created and instance.pdf:
        # Get the path to the uploaded PDF file
        pdf_path = instance.pdf.path
        
        # Convert the first page of the PDF to an image
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        
        # Get the first image (page)
        image = images[0]
        
        # Save the image in a BytesIO object to store it as an image file
        thumb_io = BytesIO()
        image.save(thumb_io, format='PNG')
        thumb_io.seek(0)
        
        # Create a new file object for the thumbnail
        thumbnail_name = f"posters/thumbnails/{instance.id}_thumb.png"
        thumbnail_file = InMemoryUploadedFile(thumb_io, None, thumbnail_name, 'image/png', thumb_io.tell(), None)
        
        # Assign the thumbnail to the instance and save it
        instance.thumbnail.save(thumbnail_name, thumbnail_file, save=False)
        instance.save()

