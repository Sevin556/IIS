from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='festivals-home'),
    path('new/', views.newFestival, name='festivals-new'),
    path('show/<int:festival_Id>/', views.show, name='festivals-show'),
    path('edit/<int:festival_Id>/', views.edit, name='festivals-edit'),
    path('delete/<int:festival_Id>/', views.delete, name='festivals-delete'),
    path('login/', views.login_view, name='festivals-login'),
    path('logout/', views.logout_view, name='festivals-logout'),
    path('register/', views.register_view, name='festivals-register'),
    path('show/new/stage/<int:festival_Id>', views.addStage, name='festivals-add-stage'),
    path('show/edit/stage/<int:stage_Id>/<int:festival_Id>/', views.editStage, name='festivals-edit-stage'),
    
    path('show/stage/manageProgram/<int:stage_Id>/f<int:festival_Id>/', views.manageProgram, name='festivals-manage-program'),
    path('show/stage/add/interpret/<int:stage_Id>/<int:interpret_Id>/<int:festival_Id>/', views.addInterpretToStage, name='festivals-add-to-stage'),
    path('show/stage/delete/interpret/<int:stage_Id>/<int:program_Id>/<int:festival_Id>/', views.deleteInterpretFromStage, name='festivals-delete-from-stage'),
    path('show/stage/edit/interpret/<int:stage_Id>/<int:program_Id>/<int:festival_Id>/', views.editInterpretStage, name='festivals-edit-interpret-stage'),
    path('show/stage/info/<int:festival_Id>/<int:stage_Id>', views.showStage, name='festivals-stage-info'),
    
    path('show/delete/stage/<int:stage_Id>/<int:festival_Id>/', views.deleteStage, name='festivals-delete-stage'),
    path('show/create/interpret/<int:festival_Id>/', views.createInterpretFestival, name='festivals-create-interpret'),
    path('show/edit/interprets/<int:festival_Id>/', views.editInterprets, name='festivals-edit-interprets'),
    path('editInterprets/add/<int:festival_Id>/<int:interpret_Id>/', views.addInterpretToFestival, name='festivals-add-interpret-to-festival'),
    path('editInterprets/delete/<int:festival_Id>/<int:interpret_Id>/', views.deleteInterpretFromFestival, name='festivals-delete-interpret-festival'),

    path('users/show/', views.showUsers, name='festivals-showUsers'),
    path("users/edit/profile/<int:user_Id>/", views.editProfile, name='festivals-edit-profile'),
    path('profile/<int:user_Id>/add_role/<str:role>/', views.add_role, name='add-role'),
    path('profile/<int:user_Id>/rem_role/<str:role>/', views.rem_role, name='rem-role'),
    path('profile/<int:user_Id>/', views.profile, name='festivals-profile'),
    path('edit-profile/<int:user_Id>', views.editProfile, name='festivals-edit-profile'),
    path('show/createTicket/<int:festival_Id>/', views.createTicketFestival, name='festivals-create-ticket-festival'),
    path('show/edit/ticket/<int:festival_Id>/<int:ticket_Id>/', views.editTicketFestival, name='festivals-edit-ticket'),

    path('show/buy/<int:festival_Id>/',views.buyTicketPage, name='festivals-buy-ticket'),
    path('profile/show/reservation/<int:res_Id>/<int:festival_Id>/', views.showReservation, name='festivals-show-reservation'),
    path('pay/reservation/<int:res_Id>/', views.payReservation, name='festivals-pay-reservation'),
    path('cancel/reservation/<int:res_Id>/', views.deleteReservation, name='festivals-delete-reservation'),
    path('confirm/reservation/<int:res_Id>/', views.confirmReservation, name='festivals-confirm-reservation'),
    path('complete/reservation/<int:res_Id>/', views.confirmReservation, name='festivals-complete-reservation'),

    path('interprets/', views.showInterprets, name='interprets-show'),
    path('create/interpret/', views.createInterpret, name='create-interpret'),
    path('interpret/profile/<int:interpret_Id>/', views.interpretProfile, name="interpret-profile"),
]
