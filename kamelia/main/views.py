import csv
import logging
import os
import random
import uuid
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404


# Локальные импорты
from .models import *
from .utils import *
from .forms import *


class YandexView(TemplateView):
    template_name = 'yandex_d263e56262d9ffc1.html'


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'
        

class Index(DataMixin, ListView):
    queryset = News.objects.order_by('-time_update')
    model = News
    template_name = 'kamelia/index.html'
    context_object_name = 'news'
    paginate_by = 6
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Домой")
        return dict(list(context.items()) + list(c_def.items()))
        
    @staticmethod
    def all_news():
    	all_news = News.objects.order_by('-time_create')
    	return all_news


class Blog(DataMixin, ListView):
	queryset = News.objects.all().reverse()
	template_name = "kamelia/blog.html"
	model = News
	context_object_name = 'news'
	paginate_by = 9
    
    	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title="Новости")
		return dict(list(context.items()) + list(c_def.items()))
    
	@staticmethod
	def news_all():
		news_all = News.objects.all().reverse()
		return news_all
		
	@staticmethod
	def all_news():
		all_news = News.objects.order_by('-time_create')
		return all_news


class ShowNews(DataMixin, DetailView):
    paginate_by = 1
    model = News
    template_name = 'kamelia/news-view.html'
    slug_url_kwarg = 'news_slug'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['news'])
        return dict(list(context.items()) + list(c_def.items()))

    @staticmethod
    def post_last3():
        post_last3 = News.objects.reverse()[:3]
        return post_last3

    @staticmethod
    def post_last6():
        post_last6 = News.objects.reverse()[:6]
        return post_last6
    
    @staticmethod
    def all_news():
    	all_news = News.objects.order_by('-time_create')
    	return all_news
		

class ContactsView(TemplateView):
    template_name = 'kamelia/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_contact = Contact.objects.filter(is_main=True).first()
        context.update({
            'main_contact': main_contact,
            'contact_groups': ContactGroup.objects.prefetch_related('contacts').all(),
        })


        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact_id = request.POST.get('contact')

        if not all([name, email, message]):
            messages.error(request, 'Пожалуйста, заполните все обязательные поля')
            return self.get(request, *args, **kwargs)

        try:
            contact = Contact.objects.get(id=contact_id) if contact_id else None
        except Contact.DoesNotExist:
            contact = None

        ContactRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
            contact=contact
        )

        messages.success(request, 'Ваше сообщение успешно отправлено!')
        return redirect('contacts')
        
    @staticmethod
    def all_news():
    	all_news = News.objects.order_by('-time_create')
    	return all_news
    	

class Conf(ListView):
    queryset = News.objects.all()
    template_name = "kamelia/conf.html"
    model = News
    
    
    @staticmethod
    def news_all_conf():
        news_all_conf = News.objects.filter(title= 'Политика конфиденциальности')
        return news_all_conf
        