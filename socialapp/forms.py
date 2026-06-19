from django import forms
from .models import Post, Comment, Profile


# -----------------------
# POST FORM
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

    # optional: improves file validation
    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            # optional safety check (you can remove if not needed)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image size should be under 5MB")

        return image


# -----------------------
# COMMENT FORM
# -----------------------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


# -----------------------
# PROFILE FORM
# -----------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

    # optional validation
    def clean_profile_picture(self):
        pic = self.cleaned_data.get('profile_picture')

        if pic:
            if pic.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image should be under 5MB")

        return pic