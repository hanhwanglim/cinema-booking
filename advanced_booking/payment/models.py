from django.db import models


# # Create your models here.

#TODO: add fields for Cards

# class Cards(models.Model):

    # def __str__(self):
    # return self.id


class CardDetails(models.Model):
    cardNumber: str = models.CharField(max_length=500, null=True)
    first4Digit = models.IntegerField(null=True)
    cardHolderFirstName = models.CharField(max_length=100, null=True)
    cardHolderLastName = models.CharField(max_length=100, null=True)
    ExpireYear = models.IntegerField(max_length=2, null=True, help_text="Please input 2 digits YY")
    ExpireMonth = models.IntegerField(max_length=2, null=True, help_text="Please input 2 digits MM")
    date_created = models.DateTimeField(auto_now_add=True, null=True)



class Order(models.Model):
    STATUS = (
        ('Unpaid', 'Unpaid'),
        ('Pending', 'Pending'),
        ('Succeed', 'Succeed'),
    )
    #TODO: add related fields

    # customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    # Movie= models.ForeignKey(Movie, null=True, on_delete=models.SET_NULL)
    # Cards_id = models.ForeignKey(Cards, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    # note = models.CharField(max_length=1000, null=True)

    # def __str__(self):
    #     return self.product.name
