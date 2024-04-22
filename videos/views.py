from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .forms import VideoPostCreateForm, VideoPostUpdateForm
from .models import VideoPost


# Create your views here.
class VideoPostDetailView(LoginRequiredMixin, DetailView):
    model = VideoPost
    template_name = 'videos/detail.html'
    context_object_name = 'video'

    def get_object(self, queryset=None):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        video_slug = self.kwargs.get('video_slug')
        try:
            video = VideoPost.objects.filter(uploaded__year=year, uploaded__month=month, uploaded__day=day,
                                             slug=video_slug)
            return video.get(Q(author=self.request.user) | Q(publish_status=True))
            # return get_object_or_404(VideoPost, uploaded__year=year, uploaded__month=month, uploaded__day=day,
            #                      slug=video_slug, publish_status=True)
        except VideoPost.DoesNotExist:
            raise Http404


class AllVideoPostListView(LoginRequiredMixin, ListView):
    template_name = 'videos/all.html'
    paginate_by = 5
    paginate_orphans = 1
    context_object_name = 'videos'
    extra_context = {'section': 'all_videos'}

    def get_queryset(self):
        return VideoPost.published.all()


class VideoPostCreateView(LoginRequiredMixin, CreateView):
    model = VideoPost
    form_class = VideoPostCreateForm
    template_name = 'videos/create.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = self.request.user
            form.save()
            messages.success(self.request, 'Video uploaded successfully!')
            return redirect('users:profile')
        return render(request, 'videos/create.html', {'form': form})


class VideoPostUpdateView(LoginRequiredMixin, UpdateView):
    model = VideoPost
    form_class = VideoPostUpdateForm
    template_name = 'videos/update.html'
    success_url = reverse_lazy('users:profile')
    context_object_name = 'video'
    query_pk_and_slug = True

    def form_valid(self, form):
        messages.info(self.request, 'Video post updated!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        return get_object_or_404(VideoPost, pk=pk, slug=slug, author=self.request.user)


class VideoPostDeleteView(LoginRequiredMixin, DeleteView):
    model = VideoPost
    template_name = 'videos/confirm_delete.html'
    success_url = reverse_lazy('users:profile')
    context_object_name = 'video'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        return get_object_or_404(VideoPost, pk=pk, slug=slug, author=self.request.user)

    def form_valid(self, form):
        messages.info(self.request, 'Video post deleted!')
        return super().form_valid(form)
