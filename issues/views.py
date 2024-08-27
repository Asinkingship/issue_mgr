from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView
)
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.urls import reverse_lazy
from .models import Issue, Status
# from django.urls import reverse


class IssueListView(ListView):                           # scan
    template_name = 'issues/list.html'
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pub_status = Status.objects.get(name="to-do")
        context["issue_list"] = (
            Issue.objects
            .filter(status=pub_status)
            .order_by("created_on").reverse()
        )
        return context
    
class DraftIssueListView(LoginRequiredMixin, ListView):
    template_name = "issues/list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft_status = Status.objects.get(name="doing")
        context["issue_list"] = (
            Issue.objects
            .filter(status=draft_status)
            .filter(author=self.request.user)
            .order_by("created_on").reverse()
        )
        return context
    
class ArchivedIssueListView(LoginRequiredMixin, ListView):
    template_name = "issues/list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        arch_status = Status.objects.get(name="done")
        context["issue_list"] = (
            Issue.objects
            .filter(status=arch_status)
            .order_by("created_on").reverse()
        )
        return context

class IssueDetailView(DetailView):                       # read single
    template_name = 'issues/detail.html'
    model = Issue

class IssueCreateView(LoginRequiredMixin, CreateView):                       # create new records
    template_name = 'issues/new.html'
    model = Issue
    fields = ['title', 'subtitle', 'body', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "issues/delete.html"
    model = Issue
    success_url = reverse_lazy("list")

    def test_func(self):
        issue = self.get_object()
        return issue.author == self.request.user

class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "issues/edit.html"
    model = Issue
    fields = ['title', 'subtitle', 'body', 'status']

    def test_func(self):
        issue = self.get_object()
        return issue.author == self.request.user
    
class IssueUpdateToDraftView(UpdateView):
    template_name = "issues/update_status.html"
    model = Issue
    fields = ["status"]
    

# Create your views here.
