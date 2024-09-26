from django.urls import path
from . import views
urlpatterns = [
    path('',views.Index,name="index"),
    path("product-list/",views.ProductList.as_view(),name='product-list'),
    path("add-product/",views.ProductAdd,name='add-product'),
    path("update-product/<int:pk>/",views.ProductUpdate.as_view(),name='update-product'),
    path("add_cart/",views.saveCart, name='add_cart'),
    path("cart-list/",views.showCart, name='cart-list'),
    path("add-order/",views.addOrder, name='add-order'),
    path("transaction-list/",views.TransactionList.as_view(), name='transaction-list'),
    path("transaction-list/<int:pk>/",views.TransactionList.as_view(), name='transaction-list'),
    path("accept-status/<int:pk>/",views.acceptStatus, name='accept-status'),
    path("deny-status/<int:pk>/",views.denyStatus, name='deny-status'),
    path("order-history/<int:uid>/",views.OrderHistoryList.as_view(), name='order-history'),
    path("order-history/<int:uid>/<int:pk>/",views.OrderHistoryList.as_view(), name='order-history'),
    path("register/",views.RegisterView,name="register"),
    path("login/", views.LoginView, name="login"),
    path("logout/", views.LogoutView, name="logout"),
    path('change_password/', views.changePasswordView, name='change_password'),
]
