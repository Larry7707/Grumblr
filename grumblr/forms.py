from django import forms

from django.contrib.auth.models import User

from grumblr.models import Post

class Registration(forms.Form):
    email = forms.EmailField(max_length = 200,
                            required = True,
                            label = "Email",
                            widget = forms.TextInput(
                                attrs={'placeholder': 'Email',
                                'class': 'form-control', "type": "Email"}))
    first_name = forms.CharField(max_length = 200, 
                                label='First Name',
                                required = True,
                                widget = forms.TextInput(
                                attrs={'placeholder': 'First NaME',
                                'class': 'form-control', "type": "First Name"}))
    last_name = forms.CharField(max_length = 200, 
                                label='Last Name',
                                required = True,
                                widget = forms.TextInput(
                                attrs={'placeholder': 'Last NamE',
                                'class': 'form-control', "type": "Last Name"}))
    username = forms.CharField(max_length = 200, 
                                label= "Username",
                                required = True,
                                widget = forms.TextInput(
                                attrs={'placeholder': 'UserName',
                                'class': 'form-control', "type": "Username"}))
    password1 = forms.CharField(max_length = 200,
                                label = "Password",
                                required = True,
                                widget = forms.PasswordInput(
                                attrs={'placeholder': 'Password',
                                'class': 'form-control', "type": "Password"})
                                )
    password2 = forms.CharField(max_length = 200,
                                label = "Confirm Password",
                                required = True,
                                widget = forms.PasswordInput(
                                attrs={'placeholder': 'Confirm Password',
                                'class': 'form-control', "type": "Password"}))

    # Customizes form validation for the username field.
    def clean(self):
        # Confirms that the username is not already present in the
        # User model database.
        cleaned_data = super(Registration, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    def clean_email(self):
        # confirm email does not exist in the user data

        # clearned_data = super(Registraion, self).clean()
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already taken.") 
        return email

    def clean_username(self):
    # confirm email does not exist in the user data

    # clearned_data = super(Registraion, self).clean()
        username = self.cleaned_data.get("username")
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.") 

        return username

class PostForm(forms.Form):
    content = forms.CharField(max_length = 42, 
                                label='Post',
                                required = True,
                                widget = forms.TextInput(
                                attrs={'placeholder': " What's Happening?",
                                'class': 'post', "type": "text", 
                                "aria-label":"Post"}))
    # Customizes form validation for the username field.

class EditProfile(forms.Form):
    first_name = forms.CharField(max_length = 200, 
                                label='First Name',
                                required = True,
                                widget = forms.TextInput(
                                attrs={'placeholder': 'First NaME',
                                'class': 'form-control', "type": "Profile"}))
    last_name = forms.CharField(max_length = 200, 
                                label='Last Name',
                                required = True,
                                widget = forms.TextInput(
                                attrs={'placeholder': 'Last NamE',
                                'class': 'form-control', "type": "Profile"}))

    bio = forms.CharField(max_length=420,
                          label="Bio",
                          required = True,
                          widget = forms.TextInput(
                                attrs={'placeholder': 'Bio',
                                'class': 'form-control', "type": "Bio"}))
    age = forms.IntegerField(min_value=0,
                            required = True,
                            widget = forms.NumberInput(
                            attrs={'placeholder': 'Age',
                            'class': 'form-control', 'type':"Profile"}))
    image = forms.ImageField(max_length=500, required=False)


class ChangePassword(forms.Form):
    password1 = forms.CharField(max_length = 200,
                                label = "Password",
                                required = True,
                                widget = forms.PasswordInput(
                                attrs={'placeholder': 'Password',
                                'class': 'form-control', "type": "Password"})
                                )
    password2 = forms.CharField(max_length = 200,
                                label = "Confirm Password",
                                required = True,
                                widget = forms.PasswordInput(
                                attrs={'placeholder': 'Confirm Password',
                                'class': 'form-control', "type": "Password"}))
    def clean(self):
        # Confirms that the username is not already present in the
        # User model database.
        cleaned_data = super(ChangePassword, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

class Comment_Form(forms.Form):
    content = forms.CharField(required=True, label="Comment",
                              widget = forms.TextInput(
                                attrs={'placeholder': 'Comment',
                                'class': 'form-control'}))