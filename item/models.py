from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(max_length=100)
    class Meta:
        ordering=('name',)
        verbose_name_plural='Categories'
    
    def __str__(self):
        return self.name

class Item(models.Model):
    category=models.ForeignKey(Category,related_name='items',on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    price=models.FloatField()
    country= models.CharField(max_length=20, choices=[('india', 'india'), ('America', 'America'), ('China', 'China')], default='India')
    district= models.CharField(max_length=20, choices=[('anantnag', 'anantnag'), ('udupi', 'udupi'), ('baramullah', 'baramullah')], default='udupi')
    village= models.CharField(max_length=20,default="karkala")
    image1=models.ImageField(upload_to='item_images',blank=True,null=True)
    image2=models.ImageField(upload_to='item_images',blank=True,null=True)
    image3=models.ImageField(upload_to='item_images',blank=True,null=True)
    is_sold=models.BooleanField(default=False)
    created_by=models.ForeignKey(User,related_name='items',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    STATE_CHOICES = [
        ('andhra_pradesh', 'Andhra Pradesh'),
        ('arunachal_pradesh', 'Arunachal Pradesh'),
        ('assam', 'Assam'),
        ('chandigarh', 'Chandigarh'),
        ('chhattisgarh', 'Chhattisgarh'),
        ('delhi', 'Delhi'),
        ('goa', 'Goa'),
        ('gujarat', 'Gujarat'),
        ('haryana', 'Haryana'),
        ('himachal_pradesh', 'Himachal Pradesh'),
        ('jammu and kashmir', 'Jammu and Kashmir'),
        ('jharkhand', 'Jharkhand'),
        ('karnataka', 'Karnataka'),
        ('kerala', 'Kerala'),
        ('ladakh', 'Ladakh'),
        ('lakshadweep', 'Lakshadweep'),
        ('madhya_pradesh', 'Madhya Pradesh'),
        ('maharashtra', 'Maharashtra'),
        ('manipur', 'Manipur'),
        ('meghalaya', 'Meghalaya'),
        ('mizoram', 'Mizoram'),
        ('nagaland', 'Nagaland'),
        ('odisha', 'Odisha'),
        ('puducherry', 'Puducherry'),
        ('punjab', 'Punjab'),
        ('rajasthan', 'Rajasthan'),
        ('sikkim', 'Sikkim'),
        ('tamil_nadu', 'Tamil Nadu'),
        ('telangana', 'Telangana'),
        ('tripura', 'Tripura'),
        ('uttar_pradesh', 'Uttar Pradesh'),
        ('uttarakhand', 'Uttarakhand'),
        ('west_bengal', 'West Bengal'),
    ]

    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='Tripura')


