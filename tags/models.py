from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItemManager(models.Manager):

    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        queryset = TaggedItem.objects.select_related('tag').filter(
            content_type=content_type,
            object_id=obj_id
        )
        return queryset

class TaggedItem(models.Model):
    # what tag is applied to what object
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)
    # product = models.ForeignKey(to=Product) # we'd need to import the product app though and this would create a dependendency
    # type (product, video, article, ...)
    # id = get the record (once we know the type)
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE) # ContentType -> generic type
    object_id = models.PositiveIntegerField() # assume all primary_keys are positive integers (which they are by default in django)
    content_object = GenericForeignKey() # now we can read the actual object which the particular tag is applied to
    objects = TaggedItemManager()