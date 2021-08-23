from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    abbreviation = models.CharField(max_length=10, null=True, blank=True, unique=True)
    warehouse_abbreviation = models.CharField(max_length=10, null=True, blank=True, unique=True)


    class Meta:
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    abbreviation = models.CharField(max_length=10, null=True, blank=True, unique=True)


    def __str__(self):
        return self.name
        

class Size(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    abbreviation = models.CharField(max_length=10, null=True, blank=True, unique=True)


    def __str__(self):
        return self.name
        

class Color(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    abbreviation = models.CharField(max_length=10, null=True, blank=True, unique=True)


    def __str__(self):
        return self.name
        

class Model(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    abbreviation = models.CharField(max_length=10, null=True, blank=True, unique=True)
    warehouse_abbreviation = models.CharField(max_length=10, null=True, blank=True, unique=True)



    def __str__(self):
        return self.name
        

class Characteristics(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True, blank=True)    
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)    
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)    
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)    


    class Meta:
        verbose_name_plural = 'Characteristics'


    def reference(self):
        return f'{self.category.abbreviation}/{self.model.abbreviation}|{self.material.abbreviation},{self.size.abbreviation},{self.color.abbreviation}'


    def __str__(self):
        if self.reference():
            return self.reference()
        else:
            return 'Reference not created'

class WarehouseLocation(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True, blank=True)
    warehouse_id = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        same_location = WarehouseLocation.objects.filter(category=self.category, model=self.model)
        self.warehouse_id = len(same_location) + 1
        print(self.warehouse_id)
        # highest_warehouse_id = max(same_location)
        super().save(*args, **kwargs)


    def reference(self):
        return f'{self.category.warehouse_abbreviation}.{self.model.warehouse_abbreviation}.{self.warehouse_id}' 


    def __str__(self):
        if self.reference():
            return self.reference()
        else:
            return 'Reference not created'



class Product(models.Model):
    characteristics = models.ForeignKey(Characteristics, on_delete=models.SET_NULL, null=True, blank=True)
    functionality = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    warehouse = models.ForeignKey(WarehouseLocation, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    reference = models.CharField(max_length=20, null=True, blank=True)
    warehouse_number = models.CharField(max_length=20, null=True, blank=True)
    date_created = models.DateField(null=True, blank=True) 

    def __str__(self):
        if self.characteristics:
            return self.title + ' ' + self.characteristics.reference()
        else:
            return self.title


    def latest_batch_id(self):
        batches = (self.batch_set.all())
        def returnID(batch):
            return batch.id
        ids = map(returnID, batches)
        ids = list(ids)
        if ids==[]:
            return None
        else:
            return max(ids)



    def update_reference(self):
        self.reference = self.characteristics.reference()
        self.save()
        return self.reference


    def assign_warehouse(self):
        if not self.warehouse:
            if self.characteristics:
                self.warehouse = WarehouseLocation.objects.create(model=self.characteristics.model, category=self.characteristics.category)
                self.warehouse_number = self.warehouse.reference()
                self.save()
                print(self.warehouse_number)
                return self.warehouse
            else:
                return 'Characteristics do not exist'
        else:
            return 'Warehouse exists'