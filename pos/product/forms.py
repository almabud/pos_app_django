from django import forms

from product.models import Category, Size, Color, Product


class AddNewProduct(forms.Form):
    GSM_CHOICES = [
        ('25', 25),
        ('30', 30),
        ('40', 40),
        ('50', 50),
        ('60', 60),
        ('70', 70),
        ('80', 80),
        ('90', 90),
        ('100', 100),
        ('110', 110)
    ]
    product = forms.ModelChoiceField(required=False, queryset=Product.objects.all(),
                                          widget=forms.Select(attrs={'class': 'form-control', 'id': 'product_select'}))
    new_product_name = forms.CharField(required=False,
                                       widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'product_input',
                                                                     'placeholder': 'Enter Product Name eg. Handle Bag'}))
    gsm = forms.ChoiceField(choices=GSM_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    product_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    bag_purchase_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    marketing_cost = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    vat = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    profit = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    transport_cost = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control', 'id': 'category_select'}))
    new_category = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'category_input',
                                                                 'placeholder': 'Enter Category eg. D-Cut'}))
    size = forms.ModelChoiceField(required=False, queryset=Size.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control', 'id': 'size_select'}))
    new_size = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'size_input',
                                                             'placeholder': 'Enter Size eg. 12/14'}))
    color = forms.ModelChoiceField(required=False, queryset=Color.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control', 'id': 'color_select'}))
    new_color = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'color_input',
                                                              'placeholder': 'Enter Color eg. Red'}))
    stock_total = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean(self):
        """If need more validation than default form validation. Then extend this method."""
        print("cleaned")
        print(self.cleaned_data)
        if 'new_product_name' in self.cleaned_data and self.cleaned_data['new_product_name']:
            print(self.cleaned_data['new_product_name'])
            if Product.objects.filter(product_name__iexact=self.cleaned_data['new_product_name']).exists():
                self.add_error('new_product_name', 'This product is already exist.')
                raise forms.ValidationError('This product is already exist.')
            self.cleaned_data['new_product'] = {
                'product_name': self.cleaned_data['new_product_name'],
                'product_description': self.cleaned_data['product_description']
            }
            del self.cleaned_data['product']
            del self.cleaned_data['new_product_name']
            del self.cleaned_data['product_description']
        else:
            if 'product' not in self.cleaned_data or not self.cleaned_data['product']:
                self.add_error('product', 'This field can\'t be empty')
                raise forms.ValidationError('Product Name can\'t be empty')
            del self.cleaned_data['product_description']
            del self.cleaned_data['new_product_name']

        if 'new_category' in self.cleaned_data and self.cleaned_data['new_category']:
            if Category.objects.filter(category__iexact=self.cleaned_data['new_category']).exists():
                self.add_error('new_category', 'This category is already exist.')
                raise forms.ValidationError('This category is already exist.')
            del self.cleaned_data['category']

        else:
            if 'category' not in self.cleaned_data or not self.cleaned_data['category']:
                self.add_error('category', 'This field can\'t be empty')
                raise forms.ValidationError('Category field can\'t be empty')
            del self.cleaned_data['new_category']

        if 'new_color' in self.cleaned_data and self.cleaned_data['new_color']:
            if Color.objects.filter(color__iexact=self.cleaned_data['new_color']).exists():
                self.add_error('new_color', 'This color is already exist.')
                raise forms.ValidationError('This color is already exist.')
            del self.cleaned_data['color']
        else:
            if 'color' not in self.cleaned_data or not self.cleaned_data['color']:
                self.add_error('color', 'This field can\'t be empty')
                raise forms.ValidationError('Color field can\'t be empty')
            del self.cleaned_data['new_color']

        if 'new_size' in self.cleaned_data and self.cleaned_data['new_size']:
            print(self.cleaned_data['new_size'])
            if Size.objects.filter(size__iexact=self.cleaned_data['new_size']).exists():
                self.add_error('new_size', 'This size is already exist.')
                raise forms.ValidationError('This size is already exist.')
            del self.cleaned_data['size']
        else:
            if 'size' not in self.cleaned_data and not self.cleaned_data['size']:
                self.add_error('size', 'This field can\'t be empty')
                raise forms.ValidationError('Size field can\'t be empty')
            del self.cleaned_data['new_size']

        return self.cleaned_data
