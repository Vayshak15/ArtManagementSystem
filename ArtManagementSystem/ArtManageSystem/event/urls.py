from django.urls import path
from event.views import index,IndexView,OpenRegistrationsView,OngoingEventView,\
    UpcomingEventView,AwaitingForResultsEventView,ResultsPublishedEventView,EventDetailView,\
    ScoreboardListView,SuggestionListView,SuggestionCreateView,SuggestionUpdateView,SuggestionDeleteView,form_handler,form_handler2




urlpatterns = [

    path('',OpenRegistrationsView.as_view(),name='open-registrations'),
    path('event/<int:pk>/',EventDetailView.as_view(),name='event-detail'),
    path('ongoing-events/', OngoingEventView.as_view(),name='ongoing-events'),
    path('upcoming-events/',UpcomingEventView.as_view(),name= 'upcoming-events'),
    path('awaiting-for-result',AwaitingForResultsEventView.as_view(),name= 'awaiting-for-result'),
    path('results-published-events/',ResultsPublishedEventView.as_view(),name= 'results-published-events'),
    path('scoreboard/',ScoreboardListView.as_view(),name='scoreboard'),
    path('sugesstion-box/', SuggestionListView.as_view(),name='suggestion-box-list'),
    path('sugesstion-box/create/', SuggestionCreateView.as_view(),name='suggestion-box-create'),
    path('sugesstion-box/<int:pk>', SuggestionUpdateView.as_view(),name='suggestion-box-update'),
    path('sugesstion-box/<int:pk>/delete/', SuggestionDeleteView.as_view(),name='suggestion-box-delete'),
    path('form-handling/',form_handler,name='form-handling'),
    path('form-handling-blog/',form_handler2,name='form-handling-blog')

]
