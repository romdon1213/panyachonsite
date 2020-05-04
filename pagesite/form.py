from django.contrib.auth.models import User
from django import forms
from ckeditor.fields import CKEditorWidget
from django.contrib.auth.forms import UserCreationForm
from social_core.backends import username, email

from pagesite.models import Post, Profile, CommentPost, CommentArticle, CommentMasalah


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=250, help_text='example@gmail.com')
    username = forms.CharField(max_length=100,
                               help_text='กรุณาตั้ง username เป็นภาษาอังกฤษไม่เกิน 150 อักษร หรือ เครื่องหมาย @/./+/-/_เท่านั้น ',
                               required=True)
    first_name = forms.CharField(label="ชื่อ", max_length=20, help_text='ชื่อที่ต้องการให้แสดงเป็นชื่อโปรไฟล์',
                                 required=True)
    # last_name = forms.CharField(label="นามสกุล", max_length=20,
    #                             help_text='ชื่อต่อท้ายที่ต้องการให้แสดงเป็นชื่อโปรไฟล์', required=True)
    password1 = forms.CharField(label='ตั้งรหัสผ่าน',
                                help_text='<ul><li>ตั้งรหัสผ่านอย่างน้อย 8 ตัวขึ้นไป</li><li>รหัสผ่านห้ามเป็นตัวเลขทั้งหมด(ต้องมีทั้งตัวเลขและตัวอักษรหรือสัญลักษณ์ เช่น @/./+/-/)</li><li>รหัสผ่านห้ามคล้ายกับชื่อ username</li></ul>',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'input-text with-border', }))  # 8 ตัวขึ้นไป,ห้ามใช้ตัวเลขล้วน,ห้ามเหมือนกับชื่อส่วนตัว
    password2 = forms.CharField(label='กรอกรหัสผ่านซ้ำอีกหนึ่งครั้ง', widget=forms.PasswordInput(attrs={
        'class': 'input-text with-border'}))

    # def clean_email(self):
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('username นี้มีผู้ใช้แล้ว')

    # def clean_email(self):
    #     if User.objects.filter(email=email):
    #         raise forms.ValidationError('email นี้มีอยู่ในระบบแล้ว')
    def clean_email(self):
        data = self.cleaned_data['email']
        duplicate_users = User.objects.filter(email=data)
        if self.instance.pk is not None:  # If you're editing an user, remove him from the duplicated results
            duplicate_users = duplicate_users.exclude(pk=self.instance.pk)
        if duplicate_users.exists():
            raise forms.ValidationError("E-mail is already registered!")
        return data
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'password1', 'password2')    #'last_name'

class UserLoginForm(forms.Form):
    username=forms.CharField(label="username / email")
    password=forms.CharField(label="password",widget=forms.PasswordInput)

class PostCreateForm(forms.ModelForm):
    body = forms.CharField(label='เขียนเนื้อหาโพสต์/บทความ', widget=CKEditorWidget(config_name='awesome'))
    title = forms.CharField(label="หัวข้อโพสต์/บทความ", required=True)

    class Meta:
        model = Post
        fields = (
            'title',
            'body',
            'category',
            'status'
        )

class PostEditForm(forms.ModelForm):
    body = forms.CharField(label='เขียนเนื้อหาโพสต์/บทความ', widget=CKEditorWidget(config_name='awesome'))
    title = forms.CharField(label="หัวข้อโพสต์/บทความ", required=True)

    class Meta:
        model = Post
        fields = (
            'title',
            'body',
            'category',
            'status'
        )

class CommentMasalahForm(forms.ModelForm):
    content=forms.CharField(label='แสดงความคิดเห็น', widget=CKEditorWidget(config_name='awesome_comment'))

    class Meta:
        model=CommentMasalah
        fields=(
            'content',
        )

class CommentPostForm(forms.ModelForm):
    content=forms.CharField(label='แสดงความคิดเห็น', widget=CKEditorWidget(config_name='awesome_comment'))

    class Meta:
        model=CommentPost
        fields=(
            'content',
        )


class CommentArticleForm(forms.ModelForm):
    content=forms.CharField(label='แสดงความคิดเห็น', widget=CKEditorWidget(config_name='awesome_comment'))

    class Meta:
        model=CommentArticle
        fields=(
            'content',
        )


class UserEditForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    first_name=forms.CharField(label='ชื่อ',max_length=30)
    # last_name = forms.CharField(label='นามสกุล', max_length=20)
    class Meta:
        model=User
        fields = ('email',
                  'username',
                  'first_name',
                  # 'last_name',
                  )
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('photo',)
        # exclude=('user',)