from functools import wraps
from decimal import Decimal
def validate_amount(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        amount=args[1] if len(args)>1 else kwargs["amount"]#allows both amount=value and value
        amount=Decimal(str(amount))
        if not amount.is_finite():
            raise ValueError("Amount must be finite")
        elif amount<=0:
            raise ValueError("Amount must be >0.")
        elif amount!=amount.quantize(Decimal("0.01")):
            raise ValueError("Amount must be entered to 2 dp.")
        
        #ensures amount=Decimal(str(amount)) is passed to the function instead of unconverted amount
        if len(args)>1:
            args=(args[0],amount,*args[2:])
        else:
            kwargs["amount"]=amount    

        result=func(*args,**kwargs)
        return result
    return wrapper

def log_operation(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print("Function started")
        result=func(*args,**kwargs)
        print("Function finished.")
        return result
    return wrapper   