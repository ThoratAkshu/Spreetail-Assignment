from django.db import models

class Product(models.Model):
    asin = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    average_rating = models.FloatField(default=0)
    total_gmv = models.FloatField(default=0)
    total_units = models.IntegerField(default=0)
    total_refunds = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.asin})"


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    week = models.CharField(max_length=20)
    units_sold = models.IntegerField()
    gmv = models.FloatField()
    refunds = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('product', 'week')



class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.product.asin} - {self.rating}"


class Return(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    return_reason = models.CharField(max_length=255)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.asin} - {self.return_reason}"

class SuggestedAction(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="suggested_action_entry")
    action_text = models.TextField()
    generated_on = models.DateTimeField(auto_now=True)
    is_manual = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {'Manual' if self.is_manual else 'Auto'}"
