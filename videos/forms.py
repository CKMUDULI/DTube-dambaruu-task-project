from django import forms

from .models import VideoPost


class VideoPostCreateForm(forms.ModelForm):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'accept': 'video/*'})
    )

    class Meta:
        model = VideoPost
        fields = ['file', 'title', 'description', 'publish_status']


class VideoPostUpdateForm(forms.ModelForm):
    class Meta:
        model = VideoPost
        fields = ['title', 'description', 'publish_status']
