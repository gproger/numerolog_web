from django.db import models
from django.contrib.auth import get_user_model
from .models import UserInfo
from django.utils.crypto import get_random_string


def createNewUser(phone, request_ip):
    userInfo = UserInfo.objects.create(
        phone=phone
    )
    last_pk = get_user_model().objects.last().pk
    email = 'dummy_user'+str(last_pk)+'@nenumerolog.ru'
    username = 'dummyuser'+str(last_pk)
    password = get_random_string(8)
    activation_kwargs = {}
    new_user = get_user_model().objects.create_user(
            username,
            email,
            password,
            create_audit_trail=True,
            joined_from_ip=request_ip,
            set_default_avatar=True,
            **activation_kwargs
        )
    userInfo.user = new_user
    userInfo.phone_valid = True
    userInfo.save()
    new_user.save()
    return new_user

    





"""
activation_kwargs = {}
    if settings.account_activation == 'user':
        activation_kwargs = {'requires_activation': UserModel.ACTIVATION_USER}
    elif settings.account_activation == 'admin':
        activation_kwargs = {'requires_activation': UserModel.ACTIVATION_ADMIN}

    try:
        new_user = UserModel.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            create_audit_trail=True,
            joined_from_ip=request.user_ip,
            set_default_avatar=True,
            **activation_kwargs
        )
    except IntegrityError:
        return Response(
            {
                '__all__': _("Please try resubmitting the form.")
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    save_user_agreements(new_user, form)
    send_welcome_email(request, new_user)

    if new_user.requires_activation == UserModel.ACTIVATION_NONE:
        authenticated_user = authenticate(
            username=new_user.email, password=form.cleaned_data['password']
        )
        login(request, authenticated_user)

    return Response(get_registration_result_json(new_user))
"""
