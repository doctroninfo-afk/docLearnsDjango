from django.db import models
from django.contrib.contenttypes.models import ContentType #Allows generic relationships
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return TaggedItem.objects \
            .select_related('tag') \
            .filter(
                content_type=content_type, 
                object_id=obj_id
    )

class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
    objects = TaggedItemManager()
    #What tag is applied to what object
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE
    )

    #Identifying the object that this tag is applied to 
    
    #Type() of an object
    #ID of the object
    #To identify any records in any table
    #Content_Type -> Which Table
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #Obect_id -> Which row
    object_id = models.PositiveIntegerField()
    #Content_object -> Actual python object
    content_object = GenericForeignKey()
