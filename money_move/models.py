from django.db import models

from django.utils import timezone, dateformat
# Create your models here.


class Income(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields

    date_today = dateformat.format(timezone.now(), 'Y-m-d')
    
    date_field = models.DateField(auto_now=False, auto_now_add=False, default=date_today)
    source = models.ForeignKey('MoneySource', on_delete=models.SET_NULL, null=True)
    ammount = models.FloatField(help_text="000.00")
    cash_kind_income = models.ForeignKey('CashKind', on_delete=models.SET_NULL, null=True)
    comment = models.TextField(help_text="Any comments?", null=True)


    

    # Metadata
    class Meta: 
        ordering = ["-date_field"]

    # Methods
    def get_absolute_url(self):

        return reverse('Income-details', args=[str(self.id)])


    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.source)


class Spendings(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields
    
    date_today = dateformat.format(timezone.now(), 'Y-m-d')

    date_field = models.DateField(auto_now=False, auto_now_add=False, default=date_today)
    kind = models.ForeignKey('SpendingKind', on_delete=models.SET_NULL, null=True)
    ammount = models.FloatField(help_text="000.00")
    cash_kind_spending = models.ForeignKey('CashKind', on_delete=models.SET_NULL, null=True)
    comment = models.TextField(help_text="Any comments?", null=True)


    

    # Metadata
    class Meta: 
        ordering = ["-date_field"]

    # Methods
    def get_absolute_url(self):

        return reverse('Spendings-details', args=[str(self.id)])
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.kind)


class MoneySource(models.Model):

    first_level_source = models.CharField(max_length=200, help_text="Source-first-level")
    second_level_source = models.CharField(max_length=200, help_text="Source-second-level")
    


    class Meta: 
        ordering = ["-first_level_source"]

    # Methods
    def get_absolute_url(self):

        return reverse('MoneySource-details', args=[str(self.id)])
    
    


    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        
        
        return str('%s %s' % (self.first_level_source, self.second_level_source))



class SpendingKind(models.Model):

    
    first_level_kind = models.CharField(max_length=200, help_text="Kind-first-level")
    second_level_kind = models.CharField(max_length=200, help_text="Kind-second-level")
    


    class Meta: 
        ordering = ["-first_level_kind"]

    # Methods
    def get_absolute_url(self):

        return reverse('SpendingKind-details', args=[str(self.id)])
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        
        
        return str('%s %s' % (self.first_level_kind, self.second_level_kind))


class Cash(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields

    date_today = dateformat.format(timezone.now(), 'Y-m-d')
    
    date_field = models.DateField(auto_now=False, auto_now_add=False, default=date_today)
    cash_kind = models.ForeignKey('CashKind', on_delete=models.SET_NULL, null=True)
    ammount = models.FloatField(help_text="000.00")
    purpose = models.BooleanField(default=False)
    comment = models.TextField(help_text="Any comments?", null=True)


    

    # Metadata
    class Meta: 
        ordering = ["-date_field"]

    # Methods
    def get_absolute_url(self):

        return reverse('Cash-details', args=[str(self.id)])


    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.cash_kind)


class CashKind(models.Model):

    
    first_level_cashkind = models.CharField(max_length=200, help_text="CashKind-first-level")
    second_level_cashkind = models.CharField(max_length=200, help_text="CashKind-second-level")
    


    class Meta: 
        ordering = ["-first_level_cashkind"]

    # Methods
    def get_absolute_url(self):

        return reverse('CashKind-details', args=[str(self.id)])
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        
        
        return str('%s %s' % (self.first_level_cashkind, self.second_level_cashkind))