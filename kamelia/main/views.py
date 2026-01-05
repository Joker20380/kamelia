import csv
import logging
import os
import random
import uuid
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.db import transaction
from django.urls import reverse




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


class RoomListView(ListView):
    model = Room
    template_name = "kamelia/room_list.html"
    context_object_name = "rooms"
    paginate_by = 12

    def get_queryset(self):
        return (Room.objects
                .select_related("category")
                .prefetch_related("amenities")
                .filter(is_published=True)
                .exclude(status=Room.STATUS_INACTIVE)
                .order_by("number"))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["all_news"] = News.objects.filter(is_published=True).order_by("-time_create")[:3]
        ctx["categories"] = RoomCategory.objects.filter(is_published=True).order_by("order", "id")
        return ctx


class RoomDetailView(DetailView):
    model = Room
    template_name = "kamelia/room_detail.html"
    context_object_name = "room"
    slug_url_kwarg = "room_slug"

    def get_queryset(self):
        return (Room.objects
                .select_related("category")
                .prefetch_related("amenities")
                .filter(is_published=True)
                .exclude(status=Room.STATUS_INACTIVE))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["all_news"] = News.objects.filter(is_published=True).order_by("-time_create")[:3]
        ctx["similar_rooms"] = (Room.objects
                                .filter(is_published=True, category=self.object.category)
                                .exclude(id=self.object.id)
                                .exclude(status=Room.STATUS_INACTIVE)
                                .order_by("number")[:3])
        return ctx


class RoomCategoryView(ListView):
    template_name = "kamelia/room_list.html"
    context_object_name = "rooms"
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        self.category = RoomCategory.objects.filter(is_published=True, slug=kwargs["category_slug"]).first()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = (Room.objects
              .select_related("category")
              .prefetch_related("amenities")
              .filter(is_published=True)
              .exclude(status=Room.STATUS_INACTIVE)
              .order_by("number"))
        if self.category:
            qs = qs.filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["category"] = self.category
        ctx["all_news"] = News.objects.filter(is_published=True).order_by("-time_create")[:3]
        ctx["categories"] = RoomCategory.objects.filter(is_published=True).order_by("order", "id")
        return ctx


def _news_footer_ctx():
    return {"all_news": News.objects.filter(is_published=True).order_by("-time_create")[:3]}


def availability_view(request):
    """
    Поиск свободных номеров по датам/гостям.
    """
    form = AvailabilitySearchForm(request.GET or None)

    rooms = Room.objects.none()
    if form.is_valid():
        checkin = form.cleaned_data["checkin"]
        checkout = form.cleaned_data["checkout"]
        adults = form.cleaned_data["adults"]
        children = form.cleaned_data["children"]
        guests = adults + children

        # занятые номера: есть бронь, пересекающаяся с интервалом
        busy_room_ids = (RoomBooking.objects
                         .exclude(status=RoomBooking.STATUS_CANCELLED)
                         .filter(date_from__lt=checkout, date_to__gt=checkin)
                         .values_list("room_id", flat=True))

        rooms = (Room.objects
                 .select_related("category")
                 .prefetch_related("amenities")
                 .filter(is_published=True)
                 .exclude(status=Room.STATUS_INACTIVE)
                 .exclude(id__in=busy_room_ids)
                 .filter(capacity__gte=guests)
                 .order_by("price", "number"))

    ctx = {
        "form": form,
        "rooms": rooms,
        "categories": RoomCategory.objects.filter(is_published=True).order_by("order", "id"),
    }
    ctx.update(_news_footer_ctx())
    return render(request, "kamelia/availability.html", ctx)


@transaction.atomic
def booking_create_view(request, room_slug):
    """
    Создание брони на номер. Даты и гости приходят querystring-ом из availability.
    """
    room = get_object_or_404(Room, slug=room_slug, is_published=True)

    # берем параметры из GET (их добавим в ссылку "забронировать")
    search_form = AvailabilitySearchForm(request.GET or None)
    if not search_form.is_valid():
        # если кто-то зашёл напрямую без дат — отправляем на поиск
        messages.warning(request, "Укажите даты заезда и выезда, чтобы оформить бронирование.")
        return redirect("availability")

    checkin = search_form.cleaned_data["checkin"]
    checkout = search_form.cleaned_data["checkout"]
    adults = search_form.cleaned_data["adults"]
    children = search_form.cleaned_data["children"]
    guests = adults + children

    if guests > room.capacity:
        messages.error(request, "Этот номер не подходит по вместимости. Выберите другой.")
        return redirect("availability")

    # повторная проверка занятости (защита от овербукинга)
    conflict_exists = (RoomBooking.objects
                       .exclude(status=RoomBooking.STATUS_CANCELLED)
                       .filter(room=room, date_from__lt=checkout, date_to__gt=checkin)
                       .exists())
    if conflict_exists:
        messages.error(request, "К сожалению, этот номер уже занят на выбранные даты.")
        return redirect("availability")

    if request.method == "POST":
        form = BookingCreateForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.date_from = checkin
            booking.date_to = checkout
            booking.adults = adults
            booking.children = children
            booking.currency = room.currency

            # расчёт цены: nights * price (минимально)
            nights = (checkout - checkin).days
            booking.total_price = room.price * nights

            booking.status = RoomBooking.STATUS_NEW
            if request.user.is_authenticated:
                booking.user = request.user

            booking.save()
            messages.success(request, "Заявка на бронирование создана. Мы свяжемся с вами.")
            return redirect("booking_success")
    else:
        form = BookingCreateForm()

    ctx = {
        "room": room,
        "form": form,
        "checkin": checkin,
        "checkout": checkout,
        "adults": adults,
        "children": children,
        "nights": (checkout - checkin).days,
        "total": room.price * ((checkout - checkin).days),
    }
    ctx.update(_news_footer_ctx())
    return render(request, "kamelia/booking_create.html", ctx)


def booking_success_view(request):
    ctx = {}
    ctx.update(_news_footer_ctx())
    return render(request, "kamelia/booking_success.html", ctx)
        