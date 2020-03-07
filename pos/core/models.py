from django.db import models, Error, IntegrityError
from scripts import employee_code_generator as code_generator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
        PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, **extra_fields):
        """Create new user with auto-generated code and password"""
        if 'name' not in extra_fields.keys():
            raise ValueError('Name must be needed')
        code = code_generator.generate_employee_code(extra_fields['name'][:2])
        if code == "":
            raise ValueError('Name must be needed')
        password = 'bd464258'
        user = self.model(code=code, **extra_fields)
        user.set_password(password)
        if 'email' in extra_fields.keys():
            email = self.normalize_email(extra_fields['email'])
            user.email = email
        try:
            user.save(using=self._db)
        except IntegrityError as e:
            raise ValueError("Testcase {}".format(e))
            # raise ValueError("Email has already been used")
        return user

    def create_superuser(self, code, password):
        """Create and save super user"""
        user = self.create_user(password=password, name=code)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    code = models.CharField(max_length=20, unique=True, blank=False, null=False, auto_created=True)
    email = models.EmailField(max_length=255, unique=True, null=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    nid = models.CharField(max_length=30, blank=True, unique=True)
    profile_pic = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    city = models.CharField(max_length=30, null=True)
    country = models.CharField(max_length=30, null=True)
    dob = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'code'
    # REQUIRED_FIELDS = ['name']
