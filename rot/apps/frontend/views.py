# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.generic import DetailView
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView

from frontend.forms import (
    AddItemForm1,
    AddItemForm2,
    AddItemForm3,
    AddItemForm4,
    SearchForm,
)
from register.models import Item
from search.indexes import ItemSearch


class ItemListView(TemplateView):
    template_name = "frontend/item/list.html"
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        page = request.GET.get('page', 1)

        form = SearchForm(self.request.GET or None)
        if form.is_valid():
            faceted_search = ItemSearch(form.cleaned_data['search'] or None, sort=form.cleaned_data['sort'] or None,
                                        filters={'categories': form.cleaned_data['category'] or None})
        else:
            faceted_search = ItemSearch(sort="name.raw")

        response = faceted_search[:faceted_search.count()].execute()

        paginator = Paginator(response, self.paginate_by)

        try:
            items = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            raise Http404('Page does not exist')

        return self.render_to_response(
            self.get_context_data(items=items, facets=response.facets or None, form=form))


class ItemDetailView(DetailView):
    template_name = "frontend/item/detail.html"
    model = Item


class AddItemWizard(SessionWizardView):
    """
    Form Wizard to add a new item

    see https://github.com/django/django-formtools/
    """
    form_list = [AddItemForm1, AddItemForm2, AddItemForm3, AddItemForm4]
    template_name = "frontend/item/wizard.html"

    def done(self, form_list, **kwargs):
        return render_to_response('frontend/item/done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
