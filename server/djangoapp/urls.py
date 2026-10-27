from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # Path for registration
    path(route='register', view=views.registration, name='register'),
    path(route='registration', view=views.registration, name='registration'),

    # Path for login and logout
    path(route='login', view=views.login_user, name='login'),
    path(route='logout', view=views.logout_request, name='logout'),

    # Path for cars
    path(route='get_cars', view=views.get_cars, name='getcars'),

    # Paths for dealerships
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),

    # Paths for reviews
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_reviews'),
    path(route='add_review', view=views.add_review, name='add_review'),

    # Path for sentiment analysis
    path(route='analyze/<str:input_txt>', view=views.analyze_sentiment, name='analyze_sentiment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
