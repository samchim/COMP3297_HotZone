from django.db import models

class Case(models.Model):
    caseNumber  = models.CharField(max_length=200)
    dateConfirmed = models.DateField()
    localOrImported = models.CharField(max_length=200)
    patientName = models.CharField(max_length=200)
    idNumber = models.CharField(max_length=200)
    dateOfBirth = models.DateField()
    virusName = models.CharField(max_length=200)
    disease = models.CharField(max_length=200) 
    maxInfectiousPeriod = models.DecimalField(max_digits=5, decimal_places=0)
    def __str__(self):
        return self.caseNumber

class LocationCache(models.Model):
    locationName = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    xCord = models.DecimalField(max_digits=6, decimal_places=0)
    yCord = models.DecimalField(max_digits=6, decimal_places=0)
    def __str__(self):
        return self.locationName

class Location(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    locationCache = models.ForeignKey(LocationCache, on_delete=models.CASCADE, null=True)
    dateFrom = models.DateField()
    dateTo = models.DateField()
    category = models.CharField(max_length=200)
    def __str__(self):
        return f'{self.case} ({self.locationCache})'