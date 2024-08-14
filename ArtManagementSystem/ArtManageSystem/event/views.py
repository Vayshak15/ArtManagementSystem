from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic import  TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib import messages
from django.urls import reverse

from event.models import Event,Registration,SuggestionBox

from event.forms import SuggestionBoxForm,BlogForm


User= get_user_model()
# Create your views here.

@login_required
def index(request):
    return render(request,'index.html')

@method_decorator(login_required, 'dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        cxt = super(IndexView, self).get_context_data(**kwargs)
        cxt['new'] = "title"
        return cxt
@method_decorator(login_required,'dispatch')
class OpenRegistrationsView(ListView):
    model = Event
    template_name = 'event/event_list.html'

    def get_queryset(self):
        return Event.objects.all().filter(registration_closes_at__gte=now()).order_by('registration_closes_at')


@method_decorator(login_required,'dispatch')
class  OngoingEventView(ListView):
    model= Event
    template_name = 'event/ongoing_event_list.html'

    def get_queryset(self):
        return Event.objects.all().filter(starts_at__lt=now(), ends_at__gt=now()).order_by('starts_at')



@method_decorator(login_required,'dispatch')
class UpcomingEventView(ListView):
    model = Event
    template_name = 'event/upcoming_event_list.html'

    def get_queryset(self):
        return Event.objects.all().filter(registration_closes_at__lte=now(),starts_at__lt=now(),).order_by('registration_closes_at')


@method_decorator(login_required,'dispatch')
class AwaitingForResultsEventView(ListView):
    model = Event
    template_name = 'event/awaiting_for_results_event_list.html'

    def get_queryset(self):
        regn_with_price_declared = Registration.objects.filter(position__isnull=False).values_list('event_id',flat=True)
        return Event.objects.all().filter(ends_at__lt=now(),).exclude(
            id__in= regn_with_price_declared
        ).order_by('registration_closes_at')

@method_decorator(login_required,'dispatch')
class ResultsPublishedEventView(ListView):
    model = Event
    template_name = 'event/result_published_event_list.html'

    def get_queryset(self):
        regn_with_price_declared = Registration.objects.filter(position__isnull=False).values_list('event_id',
                                                                                                   flat=True)
        return Event.objects.all().filter(ends_at__lt=now(),).filter(
            id__in= regn_with_price_declared).order_by('registration_closes_at')


@method_decorator(login_required,'dispatch')
class EventDetailView(DetailView):
    model = Event
    template_name = 'event/event_detail.html'

    def get_context_data(self, **kwargs):
        cxt= super(EventDetailView, self).get_context_data(**kwargs)
        cxt['is_registered'] = Registration.objects.filter(event=self.object,user=self.request.user).exists()
        return cxt

    def post(self,request,*args,**kwargs):
        self.object= self.get_object()
        reg, created= Registration.objects.get_or_create(event=self.object,user=request.user)
        if created:
            messages.success(request,f"You have sucessfully registered to {self.object.title}")
        else:
            messages.info(request, f"You are already registered to {self.object.title}")

        return self.get(request,*args,**kwargs)

@method_decorator(login_required, 'dispatch')
class ScoreboardListView(ListView):
    model = User
    template_name = 'event/scoreboard.html'

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        cxt = super(ScoreboardListView, self).get_context_data(object_list=object_list, **kwargs)
        cxt['scoreboard'] = {}
        for regn in Registration.objects.all().filter(point__gt=0):
            if regn.user not in cxt['scoreboard'].keys():
                cxt['scoreboard'][regn.user] = regn.point
            else:
                cxt['scoreboard'][regn.user] = cxt['scoreboard'][regn.user] + regn.point
        cxt['scoreboard'] = list( cxt['scoreboard'].items() )
        cxt['scoreboard'].sort(key=lambda item: item[1], reverse=True)
        return cxt


@method_decorator(login_required,'dispatch')
class SuggestionListView(ListView):
    model = SuggestionBox
    template_name = 'event/suggestionbox_list.html'


    def get_queryset(self):
        return SuggestionBox.objects.filter(user=self.request.user)

@method_decorator(login_required,'dispatch')
class SuggestionCreateView(CreateView):
    model = SuggestionBox
    #fields = ['category','description','event']
    form_class = SuggestionBoxForm

    def form_valid(self, form):
        form.instance.user= self.request.user
        return super(SuggestionCreateView,self).form_valid(form)



    def get_success_url(self):
        if self.object.category == 'Suggestions':
            msg='Thankyou for our valuable feedback!'
            messages.success(self.request, msg)
        else:
            msg = 'We have recieved your complaint! we look into it and reach back you soon!'
            messages.info(self.request, msg)

        return reverse('suggestion-box-list')

@method_decorator(login_required,'dispatch')
class SuggestionUpdateView(UpdateView):
    model = SuggestionBox
    fields = [ 'description','event']

    def get_success_url(self):
        msg = f'Your {self.object.category} sucessfully edited!'
        messages.success(self.request, msg)
        return reverse('suggestion-box-list')



@method_decorator(login_required,'dispatch')
class SuggestionDeleteView(DeleteView):
    model = SuggestionBox
    template_name = 'event/suggestionbox_confirm_delete.html'

    def get_success_url(self):
        msg = f'Your {self.object.category} sucessfully deleted!'
        messages.error(self.request, msg)
        return reverse('suggestion-box-list')

def form_handler(request):
    if request.method == 'POST':
        form = SuggestionBoxForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Sucessfully created suggestion box entry')
            return redirect('/')
    else:
        form= SuggestionBoxForm()
    context={
        'form':form
    }
    return render(request,'index.html',context)


def form_handler2(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES,)
        if form.is_valid():
            form.save()
            messages.success(request,'Sucessfully created Blog entry')
            return redirect('/')
    else:
        form= BlogForm()
    context={
        'form':form
    }
    return render(request,'index.html',context)
