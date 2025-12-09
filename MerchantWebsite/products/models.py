from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

# Validation functions 

def validate_price(value):
    if value <=0:
        raise ValidationError("Price must be greater than 0 ")
    
def validate_name(value):
    if len(value.strip()) < 2:
        raise ValidationError("Product name must be at least 2 characters")
    


# error handling so cart never breaks 

try: 
    return sum(items.get_subtotal() for item in self.items.all())
except Exception:
    return Decimal("0.00")


if self.quantity <=0:
    raise ValidatioError("Quantity must be at least 1")
# Catches error if any price or product fails will instead return 0.00 
try: 
    return self.product.price * self.quantity 
except Exception: 
    return Decimal("0.00")
