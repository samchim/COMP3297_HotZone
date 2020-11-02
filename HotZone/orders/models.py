from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return self.name

class Order(models.Model):
    time = models.DateTimeField()
    status = models.CharField(max_length=10)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    def __str__(self):
        return self.name