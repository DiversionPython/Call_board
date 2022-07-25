from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Advertisement, Reply
from .forms import AdvertisementUpdateForm, AdvertisementCreateForm, ReplyForm
from .filters import AdvertisementFilter, ReplyFilter


class AdvertisementList(ListView):
    model = Advertisement
    template_name = 'ad_list.html'
    context_object_name = 'ad'
    paginate_by = 10

class AdvertisementDetail(DetailView):

    queryset = Advertisement.objects.all()
    template_name = 'one_ad.html'
    context_object_name = 'one_ad'
    form = ReplyForm
    extra_context = {'form': ReplyForm}

    def post(self, request, *args, **kwargs):

        form = ReplyForm(request.POST)
        if form.is_valid():
            form.instance.replyAd_id = self.kwargs.get('pk')
            form.instance.replyUser = self.request.user
            form.save()

            return redirect(request.META.get('HTTP_REFERER'))


class AdvertisementCreate(LoginRequiredMixin, CreateView):
    model = Advertisement
    template_name = 'ad_create.html'
    form_class = AdvertisementCreateForm
    permission_required = ('ad_create',)

    def form_valid(self, form):
        # Автозаполнение поля user
        form.instance = self.request.user
        form.save()
        return redirect('ad_create')


class AdvertisementUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'ad_update.html'
    form_class = AdvertisementUpdateForm
    login_url = reverse_lazy('ad')
    permission_required = ('ad_update',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Advertisement.objects.get(pk=id)


class AdvertisementSearch(ListView):

    model = Advertisement
    template_name = 'ad_search.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['filter'] = AdvertisementFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ReplyList(LoginRequiredMixin, ListView):

    template_name = 'user_comment.html'
    context_object_name = 'reply'
    permission_required = ('reply',)

    def get_queryset(self, **kwargs):

        user_id = self.request.user.id
        return Reply.objects.filter(replyAd__author=user_id).filter(status_remove=False).filter(status_add=False)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context['filter'] = ReplyFilter(self.request.GET, queryset=self.get_queryset())
        context['new_response'] = Reply.objects. \
            filter(replyAd__author=user_id).filter(status_remove=False).filter(status_add=False)
        context['del_response'] = Reply.objects.filter(replyAd__author=user_id).filter(status_remove=True)
        context['add_response'] = Reply.objects.filter(replyAd__author=user_id).filter(status_add=True)
        return context


class ReplyAccept(LoginRequiredMixin, View):
    permission_required = ('accept',)

    def get(self, request, *args, **kwargs):

        pk = self.kwargs.get('pk')
        repl = Reply.objects.get(pk=pk)
        repl.status_add = 1
        repl.status_del = 0
        repl.save()

        return redirect('reply')


class ReplyRemove(LoginRequiredMixin, View):
    permission_required = ('remove',)

    def get(self, request, *args, **kwargs):

        pk = self.kwargs.get('pk')
        comm = Reply.objects.get(id=pk)
        comm.status_del = 1
        comm.status_add = 0
        comm.save()

        return redirect('reply')
