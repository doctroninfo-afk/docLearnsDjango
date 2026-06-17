from django.db import models
from django.contrib.contenttypes.models import ContentType #Allows generic relationships
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
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
