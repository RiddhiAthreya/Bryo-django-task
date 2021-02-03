# OTP-in-django
Quick and simple technique to implement the OTP functionality in your Django Project.

### Python Packages required: ```django-otp, base64, django, django-rest-framework```

I have used django-otp to generate TOTP tokens 
There are 4 main steps involved:
- Create a TOTP object.
- Use that object to generate the token.
- Take user input.
- Verify the token
Please review  the code to understand further

## API Calls

#### GET 
This is to register the mobile number into the database and generate OTP.

```http://127.0.0.1:8000/verify/9999999999/```

#### POST
This is to verify the mobile number using OTP.

```http://127.0.0.1:8000/verify/9999999999/```

Data: 
```
   {
    "otp":040301
   }
```
