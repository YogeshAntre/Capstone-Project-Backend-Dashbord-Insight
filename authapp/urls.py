


from django.urls import path
from authapp.views import JWTLoginView,LogoutView,CustomAuthUserView,ProfileView,CustomRefreshView,CustomVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
urlpatterns = [
    
    path('register/',CustomAuthUserView.as_view(),name='custom_auth_token Register'),
    path('login/',JWTLoginView.as_view(),name='custom_auth_token Login'),
    path('logout/', LogoutView.as_view(),name='custom_auth_token Logout'),
    path('profile/', ProfileView.as_view(), name="profile"),
    # path("refresh/", CustomRefreshView.as_view(), name="custom_refresh"),
    # path("verify/", CustomVerifyView.as_view(), name="token_verify"),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),# Refresh
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'), 

]