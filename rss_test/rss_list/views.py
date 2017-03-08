from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from rss_list.models import Feed


class RssListView(ListView):
    model = Feed
    template_name = 'rss_list/rss_list.html'
    context_object_name = "rss_list"
    paginate_by = 5
