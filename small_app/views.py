from django.shortcuts import render
from urllib.parse import urlencode
from django.urls import reverse
from django.http import HttpResponseRedirect
import json
import requests


authorize = 'https://oauth.vk.com/authorize?{0}'

params = {
	'client_id' : '7071736',
	'display' : 'page',
	'scope' : ['friends', 'offline'],
	'response_type' : 'code',
	'v': '5.59',
	'redirect_uri': 'https://tkapitonov.pythonanywhere.com/gettoken/',
}

sign_in_url = authorize.format(urlencode(params))

def home(request):

    return HttpResponseRedirect(sign_in_url)

def gettoken(request):
    auth_code = request.GET['code']

    params = {
        'client_id': '7071736',
        'client_secret': 'p8M433pTXB9roYduyj6a',
        'redirect_uri': 'https://tkapitonov.pythonanywhere.com/gettoken/',
        'code': str(auth_code)
    }
    authorize = 'https://oauth.vk.com/access_token?{0}'
    get_token_link = authorize.format(urlencode(params))
    r = requests.get(get_token_link)
    result = r.json()
    request.session['access_token'] = result['access_token']
    request.session['user_id'] = result['user_id']

    return HttpResponseRedirect(reverse('main'))

def main(request):

    token = request.session['access_token']
    link = 'https://api.vk.com/method/friends.get?{0}'
    params = {
        'fields' : ['first_name', 'last_name', 'city', 'domain'],
        'access_token' : str(token),
        'count': '5',
        'order': 'random',
        'v': '5.8'
        }

    get_friends_link = link.format(urlencode(params))
    user_friends=requests.get(get_friends_link)
    users = user_friends.json()['response']['items']


    user_link = 'https://api.vk.com/method/users.get?{0}'
    current_user_id = request.session['user_id']
    user_params = {
        'fields' : ['first_name', 'last_name', 'city', 'domain'],
        'current_user_id': str(current_user_id),
        'access_token' : str(token),
        'v': '5.8'
        }
    get_user_info_link = user_link.format(urlencode(user_params))

    user_info = requests.get(get_user_info_link)
    current_user = user_info.json()['response'][0]
    print(current_user)
    context = {
        'users': users,
        'current_user': current_user
        }

    return render(request, 'small_app/main.html', context)
