from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from dostawemo.users import views as users_views
from dostawemo.purchases import views as purchases_views
from dostawemo.products import views as products_views
from dostawemo.carts import views as carts_views
from dostawemo.orders import views as orders_views
from dostawemo.questions import views as questions_views
from dostawemo.feedback import views as feedback_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', users_views.UserViewSet, basename='user')
router.register(r'groups', users_views.GroupViewSet)
router.register(r'purchases', purchases_views.PurchaseViewSet)
router.register(r'products', products_views.ProductViewSet)
router.register(r'categories', products_views.CategoryViewSet)
router.register(r'colors', products_views.ColorViewSet)
router.register(r'sizes', products_views.SizeViewSet)
router.register(r'carts', carts_views.CartViewSet, basename='cart')
router.register(r'carts/items', carts_views.CartItemViewSet)
router.register(r'orders/payment', orders_views.PaymentViewSet, basename='payment')
router.register(r'orders/prepayment', orders_views.PrepaymentViewSet, basename='prepayment')
router.register(r'orders', orders_views.OrderViewSet, basename='order')
router.register(r'images/products', products_views.ProductImageViewSet)
router.register(r'questions', questions_views.QuestionViewSet)
router.register(r'feedback', feedback_views.FeedbackViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^markdownx/', include('markdownx.urls')),
]

urlpatterns += [
    path('api/orders/fail-prepayment/', orders_views.FailPrepaymentView),
    path('api/orders/success-prepayment/', orders_views.SuccessPrepaymentView),
    path('api/orders/fail-payment/', orders_views.FailPaymentView),
    path('api/orders/success-payment/', orders_views.SuccessPaymentView),
]

urlpatterns += [
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += [
    path('api/token/code/', users_views.SendCode.as_view(), name='token_obtain_pair'),
    path('api/token/', users_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)