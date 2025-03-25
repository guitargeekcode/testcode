from rest_framework.routers import DefaultRouter
from account.views.login import ProtectedView
from account.views.login import AuthAPIView
router = DefaultRouter()
router.register(r'auth', AuthAPIView, basename='auth')
router.register(r'protected',ProtectedView,basename="protected")
