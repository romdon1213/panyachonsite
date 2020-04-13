from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    email=forms.EmailField(max_length=250,help_text='example@gmail.com')
    username = forms.CharField(max_length=100, help_text='กรุณาตั้ง username เป็นภาษาอังกฤษไม่เกิน 150 อักษร หรือ เครื่องหมาย @/./+/-/_เท่านั้น ', required=True)
    first_name=forms.CharField(max_length=100,help_text='ชื่อที่ต้องการให้แสดงเป็นชื่อโปรไฟล์',required=True)
    last_name = forms.CharField(max_length=100, help_text='ชื่อต่อท้ายที่ต้องการให้แสดงเป็นชื่อโปรไฟล์', required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'input-text with-border', 'placeholder': '8ตัวขึ้นไป/ห้ามตัวเลขล้วน/ไม่คล้ายกับชื่อส่วนตัว'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input-text with-border', 'placeholder': 'กรอสรหัสซ้ำอีกครั้งหนึ่ง'}))
    class Meta :
        model=User
        fields=('email','username','first_name','last_name','password1','password2')