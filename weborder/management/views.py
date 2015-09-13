# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.http import Http404
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import *


@login_required
def cart(req):
    user = MyUser.get_user(req.session.get('username', ''))
    if user == '':
        return login(req)
    item_list = Cart.objects.filter(user=user)
    sum_price, sum_weight, sum_count = 0, 0, 0
    if item_list.exists():
        for item in item_list:
            sum_price += item.item_id.price * item.count
            sum_weight += item.item_id.weight * item.count
            sum_count += item.count
    content = {'active_menu': 'cart',
               'user': user,
               'cart_count': Cart.get_cart_count(user),
               'item_list': item_list,
               'sum_price': sum_price,
               'sum_weight': sum_weight,
               'sum_count': sum_count,
               }

    return render_to_response("cart.html", content)


def home(req):
    user = MyUser.get_user(req.session.get('username', ''))
    content = dict(active_menu='homepage',
                   user=user, img_list=HomeImg.objects.all(),
                   cart_count=Cart.get_cart_count(user))
    return render_to_response("home.html", content)


def about(req):
    user = MyUser.get_user(req.session.get('username', ''))
    content = {'active_menu': 'about',
               'user': user,
               'cart_count': Cart.get_cart_count(user),
               }
    return render_to_response("about.html", content)


def index(req):
    user = MyUser.get_user(req.session.get('username', ''))
    content = {'active_menu': 'homepage',
               'user': user,
               'img_list': HomeImg.objects.all(),
               'cart_count': Cart.get_cart_count(user),
               }
    return render_to_response('index.html', content)


def signup(req):
    if req.session.get('username', ''):
        return HttpResponseRedirect('/')
    status = ''
    if req.POST:
        post = req.POST
        passwd = post.get('passwd', '')
        repasswd = post.get('repasswd', '')
        if passwd != repasswd:
            status = 're_err'
        else:
            username = post.get('username', '')
            if User.objects.filter(username=username):
                status = 'user_exist'
            else:
                newuser = User.objects.create_user(username=username, password=passwd, email=post.get('email', ''))
                newuser.save()
                new_myuser = MyUser(user=newuser, nickname=post.get('nickname'), permission=1)
                new_myuser.save()
                status = 'success'
    content = {'active_menu': 'homepage', 'status': status, 'user': ''}
    return render_to_response('signup.html', content, context_instance=RequestContext(req))


def is_already_login(username):  # 防止重复登录
    try:
        user = MyUser.objects.get(user__username=username)
        if user:
            return False
            return not user.user.is_authenticated()
        else:
            return False
    except MyUser.DoesNotExist:
        return False


def login(req):
    print 'login'
    if req.session.get('username', ''):
        return HttpResponseRedirect('/')
    next_page = req.GET.get('next', '')
    print next_page
    status = ''
    if req.POST:
        post = req.POST
        username = post.get('username', '')
        if is_already_login(username):
            status = 'login_at_other_place'
        else:
            password = post.get('passwd', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(req, user)
                    req.session['username'] = username
                    if next_page:
                        # return view(req)
                        return HttpResponseRedirect(next_page)
                    return HttpResponseRedirect('/view/')
                else:
                    status = 'not_active'
            else:
                status = 'not_exist_or_passwd_err'
    content = {'active_menu': 'homepage', 'status': status, 'user': ''}
    return render_to_response('login.html', content, context_instance=RequestContext(req))


@login_required
def logout(req):
    auth.logout(req)
    return HttpResponseRedirect('/')


@login_required
def setpassword(req):
    user = MyUser.get_user(req.session.get('username', ''))
    if user == '':
        return HttpResponseRedirect('/login/')
    status = ''
    if req.POST:
        post = req.POST
        if user.user.check_password(post.get('old', '')):
            if post.get('new', '') == post.get('new_re', ''):
                user.user.set_password(post.get('new', ''))
                user.user.save()
                status = 'success'
            else:
                status = 're_err'
        else:
            status = 'passwd_err'
    content = {'user': user,
               'active_menu': 'user_menu',
               'status': status,
               'cart_count': Cart.get_cart_count(user),
               }
    return render_to_response('setpasswd.html', content, context_instance=RequestContext(req))


def add(req):
    username = req.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        return HttpResponseRedirect('/login/')
    if user.permission < 2:
        return HttpResponseRedirect('/')
    status = ''
    if req.POST:
        post = req.POST
        newbook = Instruments(
            name=post.get('name', ''),
            author=post.get('author', ''),
            typ=post.get('typ', ''),
            price=post.get('price', ''),
            pubDate=post.get('pubdate', ''),
        )
        newbook.save()
        status = 'success'
    content = {'user': user, 'active_menu': 'addbook', 'status': status}
    return render_to_response('add.html', content, context_instance=RequestContext(req))


@login_required
def history(req):
    usr = MyUser.get_user(req.session.get('username', ''))
    if usr == '':
        return login(req)
    order_lists = OrderList.objects.filter(user=usr)
    content = {'active_menu': 'history',
               'user': usr,
               'cart_count': Cart.get_cart_count(usr),
               'order_list': order_lists,
               }
    return render_to_response("history.html", content)


@login_required
def order_list(req):
    user = MyUser.get_user(req.session.get('username', ''))
    if user == '':
        return login(req)
    order_id = req.GET.get('order_id', '')
    if order_id == '':
        return HttpResponseRedirect('/history/')
    have_order = False
    order_info = ''
    if OrderList.objects.filter(pk=order_id).exists():
        have_order = True
        order_info = OrderList.objects.get(pk=order_id)
    try:
        order_items = OrderDetail.objects.filter(order_id__id=order_id)
    except OrderDetail.DoesNotExist:
        return history(req)
        # return HttpResponseRedirect('/history/')
    content = {'user': user,
               'active_menu': 'user_menu',
               'order_items': order_items,
               'order_info': order_info,
               'have_order': have_order,
               'cart_count': Cart.get_cart_count(user),
               }
    return render_to_response('orderlist.html', content)


@login_required
def view(req):
    user = MyUser.get_user(req.session.get('username', ''))
    if user == '':
        return login(req)
    type_list = Instruments.get_type_list()
    book_type = req.GET.get('type', 'all')
    if book_type == '':
        book_lst = Instruments.objects.all()
    elif book_type not in type_list:
        book_type = 'all'
        book_lst = Instruments.objects.all()
    else:
        book_lst = Instruments.objects.filter(typ=book_type)

    if req.POST:
        post = req.POST
        keywords = post.get('keywords', '')
        book_lst = Instruments.objects.filter(name__contains=keywords)
        book_type = 'all'

    paginator = Paginator(book_lst, 5)
    page = req.GET.get('page')
    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)

    content = {'user': user,
               'active_menu': 'viewpage',
               'type_list': type_list,
               'book_type': book_type,
               'book_list': book_list,
               'cart_count': Cart.get_cart_count(user),
               }
    return render_to_response('view.html', content, context_instance=RequestContext(req))


@login_required
def order(req):
    usr = MyUser.get_user(req.session.get('username', ''))
    if usr == '':
        return HttpResponseRedirect("/login/")
    maxnum = int(req.GET.get("maxnum", 0))
    address = req.GET.get("address", "no place")
    transport = req.GET.get("transport", "no way")
    print maxnum, ' maxnum'
    order_data = []
    for i in range(1, maxnum + 1):
        cart_item_id = int(req.GET.get("cart_itemid_name_" + str(i), -1))
        cart_item_amount = int(req.GET.get("cart_amount_name_" + str(i), -1))
        if cart_item_id != -1 and Instruments.check_item_id(cart_item_id, cart_item_amount):
            order_data.append((cart_item_id, cart_item_amount))
    order_num = len(order_data)
    if order_num > 0:
        new_order = OrderList.objects.create(
            user=usr,
            sum_price=0,
            weight=0,
            address=address,
            transport=transport,
            date=datetime.now(),
        )
        sum_price, sum_weight = 0.0, 0.0
        for data in order_data:
            cur_item = Instruments.objects.get(pk=data[0])
            new_detail = OrderDetail.objects.create(
                order_id=new_order,
                item_id=cur_item,
                count=data[1],
                price=cur_item.price*data[1],
                weight=cur_item.weight*data[1],
            )
            sum_weight += new_detail.weight
            sum_price += new_detail.price
            cur_item.count -= data[1]
            cur_item.save(force_update=True)
            Cart.objects.get(user=usr, item_id=cur_item).delete()
        new_order.sum_price = sum_price
        new_order.weight = sum_weight
        new_order.save(force_update=True)
        content = {'user': usr,
                   'active_menu': 'user_menu',
                   'order_items': OrderDetail.objects.filter(order_id=new_order),
                   'cart_count': Cart.get_cart_count(usr),
                   }
        return render_to_response('orderlist.html', content)
    return HttpResponseRedirect("/history/")


@login_required
def add_to_cart(req):
    usr = MyUser.get_user(req.session.get('username', ''))
    if usr == '':
        return login(req)
    amount = req.GET.get("amount", -1)
    instrument_id = req.GET.get("id", -1)
    try:
        instrument_id = int(instrument_id)
    except ValueError:
        instrument_id = -1
    try:
        amount = int(amount)
    except ValueError:
        amount = -1
    if instrument_id < 0:
        return HttpResponseRedirect('/view/')
    if amount <= 0:
        return HttpResponseRedirect('/view/?id=' + str(instrument_id))
    try:
        item = Cart.objects.get(user=usr, item_id__id=instrument_id)
    except Cart.DoesNotExist:
        item = ''
    instrument = Instruments.objects.get(pk=instrument_id)
    print instrument
    if item == '':
        if instrument == '':
            return HttpResponseRedirect('/view/')
        Cart.objects.create(user=usr,
                            item_id=instrument,
                            price=instrument.price * amount,
                            weight=instrument.weight * amount,
                            count=amount)
    else:
        amount += item.count
        item.count = amount
        item.weight = instrument.weight * amount
        item.price = instrument.price * amount
        item.save(force_update=True)
    return HttpResponseRedirect('/view/')


@login_required
def delete_from_cart(req):
    user = MyUser.get_user(req.session.get('username', ''))
    if user == '':
        return login(req)
    del_item_id = req.GET.get("cart_item_id", '')
    print del_item_id
    if del_item_id == ' ':
        return HttpResponseRedirect("/cart/")
    else:
        Cart.objects.filter(user=user, id=del_item_id).delete()
        return HttpResponseRedirect("/cart/")


def detail(req):
    user = MyUser.get_user(req.session.get('username', ''))
    if user == '':
        return login(req)
    item_id = req.GET.get('id', '')
    if item_id == '':
        return HttpResponseRedirect('/view/')
    try:
        instrument = Instruments.objects.get(pk=item_id)
    except Instruments.DoesNotExist:
        return HttpResponseRedirect('/view/')
    img_list = Img.objects.filter(item=instrument)
    content = {'user': user,
               'active_menu': 'viewpage',
               'book': instrument,
               'img_list': img_list,
               'cart_count': Cart.get_cart_count(user),
               }
    return render_to_response('detail.html', content)
