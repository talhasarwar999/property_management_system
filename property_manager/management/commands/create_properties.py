from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image as PILImage
import io
import random
import os

from property_manager.models import Property, Image, Document, PropertyDealer, Broker

class Command(BaseCommand):
    help = 'Populates the database with dummy Property records along with related Images and Documents.'


    def handle(self, *args, **options):
        for _ in range(50):
            # Assume PropertyDealer and Broker are populated or create dummy ones as needed
            owner = PropertyDealer.objects.get(user__username='saad')
            # broker, _ = Broker.objects.get_or_create(name="Dummy Broker", defaults={'details': 'Dummy broker details'})

            # Generate and save a dummy image
            img = PILImage.new('RGB', (100, 100), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG')
            img_file = ContentFile(img_io.getvalue(), 'dummy.jpg')



            image = Image()
            image.image.save('dummy.jpg', img_file)
            image.description = "Dummy image description"
            image.save()

            # Generate and save a dummy document
            doc_content = 'This is a dummy document content.'
            doc_file = ContentFile(doc_content.encode('utf-8'), 'dummy.txt')

            document = Document()
            document.file.save('dummy.txt', doc_file)
            document.description = "Dummy document description"
            document.save()

            # Create a dummy Property with all fields populated
            property = Property(
                owner=owner,
                title=f'Dummy Property {_}',
                address=f'{random.randint(100, 999)} Fake Street, Faketown',
                property_type=random.choice(['rented', 'sold', 'free', 'off-plan']),
                status=random.choice(['available', 'not available']),
                location='Dummy Location',
                country='Dummyland',
                city='Dummy City',
                state='Dummy State',
                est_rent=random.uniform(1000, 5000),
                total_area=random.uniform(100, 1000),
                num_rooms=random.randint(1, 10),
                num_bathrooms=random.randint(1, 5),
                est_delivery_time=timezone.now(),
                construction_year=random.randint(1990, 2020),
                has_swimming_pool=random.choice([True, False]),
                has_garden=random.choice([True, False]),
                has_garage=random.choice([True, False]),
                listing_details='Dummy listing details with all features and amenities.'
            )
            property.save()
            property.images.add(image)
            property.documents.add(document)

            self.stdout.write(self.style.SUCCESS(f'Successfully created Property "{property.title}" with all fields populated and associated Image and Document.'))
