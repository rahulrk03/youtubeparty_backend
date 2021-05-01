from django.shortcuts import render


def user_list(request):
    return render(request, 'chat/user_list.html')