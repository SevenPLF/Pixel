from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django import forms
from PixelProject.settings import MEDIA_ROOT, MEDIA_URL
from pixel.models import Pixel_C as pp, lable, Follow, Pixel_B, Pixel_A, UserProfile, Pixel_W, User as uuuu
from django.http import JsonResponse, HttpResponse
from django.db.models import Max, Func
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
from .forms import SearchForm
from django.db.models import Q
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import uuid, os

# from .models import UserInfo

# Create your views here.
# 登录
def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        addflag = False
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    user_info, created = User.objects.get_or_create(username=user)
                    userinfo = UserProfile.objects.get(user_id=user)
                    # 获取当前日期
                    naive_dt = datetime.now()
                    current_date = timezone.make_aware(naive_dt, timezone.get_current_timezone()).strftime("%Y-%m-%d")
                    # 检查用户上一次登录日期是否为今天
                    if not user.last_login or (user_info.last_login + timedelta(hours=8)).strftime(
                            "%Y-%m-%d") < current_date:
                        addflag = True
                    login(request, user)
                    # msg="登录成功"
                    request.session['status'] = True
                    request.session['uname'] = username
                    request.session.set_expiry(300)
                    if addflag:
                        userinfo.user_points += 100
                        userinfo.user_experience += 10
                        userinfo.save()
                return redirect("/index/", request)
            else:
                msg = "用户名密码错误"
                return render(request, "login.html", locals())

        else:
            msg = "用户名不存在"
            return render(request, "login.html", locals())

    return render(request, "login.html", locals())


# 注册
def regView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        lxdh = request.POST.get("lxdh")

        if len(username) < 1:
            msg = "用户名不能为空"
        elif len(username) > 16:
            msg = "用户名超长（最长16位）"
        elif len(password) < 1:
            msg = "密码不能为空"
        elif len(password) >= 1 and len(password) < 5:
            msg = "密码最少6位"
        elif len(password) > 13:
            msg = "密码最大12位"
        elif User.objects.filter(username=username):
            msg = "用户名已存在"
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            UserProfile.objects.create(user=user, user_level=0, user_points=1000, user_experience=0,
                                       is_realname_authenticated=False, mobile_number=lxdh,)
            msg = "注册成功"
            return redirect("/login/")
    return render(request, "register.html", locals())



class MaxZForUpdate(Func):
    function = 'GREATEST'
    template = '%(function)s(%(expressions)s)'


from django.shortcuts import get_object_or_404


def add_points(request, user_id, points):
    profile = get_object_or_404(Profile, user_id=user_id)
    profile.points += points
    profile.save()
    return HttpResponse("Points added successfully.")

@login_required
@csrf_exempt
@login_required
def upload_avatar(request):
    if request.method == 'POST':
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            # 使用用户ID创建子文件夹名称
            user_folder = f"{request.user.id}"
            fs = FileSystemStorage(location=os.path.join(MEDIA_ROOT, 'avatars', user_folder))

            # 创建子文件夹路径
            full_path = os.path.join(fs.location)
            if not os.path.exists(full_path):
                os.makedirs(full_path)

            # 清空子文件夹下的所有文件
            for file_name in os.listdir(full_path):
                file_path = os.path.join(full_path, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)

            # 生成唯一的文件名
            file_name = f"{uuid.uuid4()}.{avatar.name.split('.')[-1]}"
            filename = fs.save(file_name, avatar)
            # uploaded_file_url = fs.url(filename)
            user_info = UserProfile.objects.get(user_id=request.user.id)
            user_info.avatar_url = f"{MEDIA_URL}avatars/{user_folder}/{filename}"
            user_info.save()
            return JsonResponse({'url': f"{MEDIA_URL}avatars/{user_folder}/{filename}"})
        else:
            return JsonResponse({'error': 'No avatar file provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def add_button(request, id):
    try:
        if id >= 20001 and id <= 30000:
            abc = Pixel_A
        elif id >= 30001 and id <= 40000:
            abc = Pixel_B
        elif id >= 10001 and id <= 20000:
            abc = pp

        update_list, value_list, lable_list, user_list, deltime_list = udzl(abc.objects.get(id=id))
        user_u = user_list[update_list.index(max(update_list))]
        label = lable_list[update_list.index(max(update_list))]
        value_c = value_list[update_list.index(max(update_list))]
        deltime = deltime_list[update_list.index(max(update_list))]

        # 根据传入的 id 查询数据库中的数据
        color_number = value_c
        if color_number == 0:
            color_number = '2039326'
        user_points = UserProfile.objects.get(user_id=request.user.id)
        if user_points.user_points < 1:
            return JsonResponse({'success': False, 'error': 'Data not found'})
        user_points.user_experience += 1
        user_points.user_points -= 1
        user_points.save()
        if id >= 20001 and id <= 30000:
            abc = Pixel_A
            lable(
                user_id=uuuu.objects.get(id=user_u),
                pixel_id=id,
                lable_text=label,
                del_time=deltime,
                lable_url='',
                index_abc='Pixel_A',
                z=color_number,
                add_user_id=request.user, ).save()
        elif id >= 30001 and id <= 40000:
            abc = Pixel_B
            lable(
                user_id=uuuu.objects.get(id=user_u),
                pixel_id=id,
                lable_text=label,
                del_time=deltime,
                lable_url='',
                index_abc='Pixel_B',
                z=color_number,
                add_user_id=request.user, ).save()
        elif id >= 1 and id <= 10000:
            abc = pp
            lable(
                user_id=uuuu.objects.get(id=user_u),
                pixel_id=id,
                lable_text=label,
                del_time=deltime,
                lable_url='',
                index_abc='Pixel_C',
                z=color_number,
                add_user_id=request.user, ).save()

        button_pp = abc.objects.get(id=id)
        index = udzl(button_pp, insert_flag=True, insert_flag2=True)
        if index == 1:
            button_pp.del_time1 = int(deltime) + 3600
        elif index == 2:
            button_pp.del_time2 = int(deltime) + 3600
        elif index == 3:
            button_pp.del_time3 = int(deltime) + 3600

        button_pp.save()

        data = {'user_points': user_points.user_points, 'user_experience': user_points.user_experience}
        return JsonResponse({'success': True, 'data': data})
    except lable.DoesNotExist:
        return JsonResponse({'error': 'Data not found'}, status=404)

@login_required
def process_data(request, id):
    try:
        # 根据传入的 id 查询数据库中的数据
        text_lable = request.POST.get('text')
        color_number = int(str(request.POST.get('color')[1:]), 16)
        if color_number == 0:
            color_number = '2039326'
        lasttime = int(request.POST.get('lasttime'))
        user_points = UserProfile.objects.get(user_id=request.user.id)
        if user_points.user_points - lasttime < 0:
            return JsonResponse({'success': False, 'error': 'Data not found'})
        user_points.user_experience += 1
        user_points.user_points -= lasttime
        user_points.save()
        lasttime *= 3600
        naive_dt = datetime.now()
        current_system_time = timezone.make_aware(naive_dt, timezone.get_current_timezone())
        if id >= 20001 and id <= 30000:
            abc = Pixel_A
            lable(
                user_id=request.user,
                pixel_id=id,
                lable_text=text_lable,
                del_time=lasttime,
                lable_url='',
                index_abc='Pixel_A',
                z=color_number, ).save()
        elif id >= 30001 and id <= 40000:
            abc = Pixel_B
            lable(
                user_id=request.user,
                pixel_id=id,
                lable_text=text_lable,
                del_time=lasttime,
                lable_url='',
                index_abc='Pixel_B',
                z=color_number, ).save()
        elif id >= 1 and id <= 10000:
            abc = pp
            lable(
                user_id=request.user,
                pixel_id=id,
                lable_text=text_lable,
                del_time=lasttime,
                lable_url='',
                index_abc='Pixel_C',
                z=color_number, ).save()

        button_pp = abc.objects.get(id=id)
        index = udzl(button_pp, insert_flag=True, insert_flag2=False)
        if index == 0:
            button_pp.u1 = request.user.id
            button_pp.z1 = color_number
            button_pp.lable1 = text_lable
            button_pp.update_time1 = current_system_time
            button_pp.del_time1 = lasttime
        elif index == 1:
            button_pp.u2 = request.user.id
            button_pp.z2 = color_number
            button_pp.lable2 = text_lable
            button_pp.update_time2 = current_system_time
            button_pp.del_time2 = lasttime
        elif index == 2:
            button_pp.u3 = request.user.id
            button_pp.z3 = color_number
            button_pp.lable3 = text_lable
            button_pp.update_time3 = current_system_time
            button_pp.del_time3 = lasttime

        button_pp.save()

        data = {'user_points': user_points.user_points, 'user_experience': user_points.user_experience}
        # data = lable.objects.get(id=id)
        # 将数据转换为 JSON 格式
        # data.serialize()

        return JsonResponse({'success': True, 'data': data})
    except lable.DoesNotExist:
        return JsonResponse({'error': 'Data not found'}, status=404)


@login_required
def get_label_data(request, pixel_id):
    if request.method == "GET":
        try:
            if pixel_id >= 10001 and pixel_id <= 20000:
                aa = Pixel_W.objects.get(id=pixel_id)
                bb = UserProfile.objects.get(user=request.user)
                if bb.user_points - 1 < 0:
                    bb.user_points = -1
                    data_pp = {'user_points': bb.user_points, 'user_experience': bb.user_experience}
                    return JsonResponse({'success': True, 'data': ('0', list(request.GET.values())[1], data_pp)})
                else:
                    bb.user_points -= 1
                    bb.user_experience += 1
                bb.save()

                color_number = int(str(list(request.GET.values())[1][1:]), 16)

                if color_number == 0:
                    color_number = '2039326'

                aa.z1 = color_number

                aa.save()
                data_pp = {'user_points': bb.user_points, 'user_experience': bb.user_experience}

                return JsonResponse({'success': True, 'data':('0', list(request.GET.values())[1], data_pp), 'pixel_id': pixel_id,'hours_difference': 0})

            elif pixel_id >= 20001 and pixel_id <= 30000:
                abc = Pixel_A
            elif pixel_id >= 30001 and pixel_id <= 40000:
                abc = Pixel_B
            else:
                abc = pp

            update_list, value_list, lable_list, user_list, deltime_list = udzl(abc.objects.get(id=pixel_id))
            user_u = user_list[update_list.index(max(update_list))]
            label = lable_list[update_list.index(max(update_list))]
            deltime = deltime_list[update_list.index(max(update_list))]
            naive_dt = datetime.now()
            try:
                current_system_time = timezone.make_aware(naive_dt, timezone.get_current_timezone())
                new_datetime = max(update_list) + timedelta(seconds=int(deltime))
                hours_difference = round((new_datetime - current_system_time) / timedelta(hours=1),2)
            except:
                hours_difference = 0.0

            level = 0
            if user_u == 'a':
                uuu = '0'
                uu = '0'
            else:
                uuu = UserProfile.objects.filter(user=user_u).values()[0]
                uu = User.objects.get(pk=uuu['user_id']).username
                print(UserProfile.objects.filter(user=user_u).values())

                level = UserProfile.objects.filter(user=user_u).values()[0]['user_level']
            is_followed = 0
            fans_count = 0
            following_count = 0
            if user_u != 'a':
                is_followed = Follow.objects.filter(followed_id=user_u, follower_id=request.user.id).count()
                fans_count = Follow.objects.filter(followed_id=user_u).count()
                following_count = Follow.objects.filter(follower_id=user_u).count()
            return JsonResponse({'success': True, 'data': (label, len(update_list), uu, uuu, fans_count, following_count, is_followed, request.user.id), 'url': uuu['avatar_url'] if 'avatar_url' in uuu and uuu['avatar_url'] else None, 'pixel_id': pixel_id, 'hours_difference': hours_difference, 'level': level,})
        except lable.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Label not found for pixel_id'})
    return JsonResponse({'success': False})


def udzl(p_button, insert_flag=False, insert_flag2=False):
    naive_dt = datetime.now()
    current_system_time = timezone.make_aware(naive_dt, timezone.get_current_timezone())
    update_list = []
    value_list = []
    lable_list = []
    user_list = []
    deltime_list = []
    index = 0
    for u, d, z, l, i in zip([p_button.update_time1, p_button.update_time2, p_button.update_time3],
                             [p_button.del_time1, p_button.del_time2, p_button.del_time3],
                             [p_button.z1, p_button.z2, p_button.z3],
                             [p_button.lable1, p_button.lable2, p_button.lable3],
                             [p_button.u1, p_button.u2, p_button.u3]
                             ):

        new_datetime = u + timedelta(seconds=d)
        if current_system_time > new_datetime:
            if insert_flag:
                return index
            continue
        elif u not in update_list:
            update_list.append(u)
            value_list.append(z)
            lable_list.append(l)
            user_list.append(i)
            deltime_list.append(d)
        index += 1
    if insert_flag and insert_flag2:
        return index
    if value_list == []:
        value_list.append(4294967295)
        update_list.append(0)
        lable_list.append('')
        user_list.append('a')
        deltime_list.append(0)
    return update_list, value_list, lable_list, user_list, deltime_list



@login_required
@require_POST
def biaoqian(request):
    query = request.POST.get('q', '')
    if query == '':
        return JsonResponse([], safe=False)
    if query == 'dianying':
        abc = Pixel_A
    elif query >= 'shehui':
        abc = Pixel_B
    else:
        abc = pp
    p_buttons_content_game = []
    if query != 'baiban':
        for p_button in abc.objects.all():
            update_list, value_list, lable_list, user_list, deltime_list= udzl(p_button)
            if hex(int(value_list[update_list.index(max(update_list))]))[2:] == 0:
                max_value = '#120202'
            else:
                max_value = '#' + hex(int(value_list[update_list.index(max(update_list))]))[2:]
            p_buttons_content_game.append({'button': p_button.id, 'color': max_value, 'count_c': len(update_list)})
    else:
        for p_button in Pixel_W.objects.all():
            if hex(int(p_button.z1))[2:] == 0:
                max_value = '#120202'
            else:
                max_value = '#' + hex(int(p_button.z1))[2:]
            p_buttons_content_game.append({'button': p_button.id, 'color': max_value, 'count_c': 3})
    return JsonResponse(p_buttons_content_game, safe=False)


@login_required
@require_POST
def search(request):
    query = request.POST.get('q', '')
    if query == '':
        return JsonResponse([], safe=False)

    results0 = pp.objects.filter(
        Q(lable1__icontains=query) |
        Q(lable2__icontains=query) |
        Q(lable3__icontains=query)
    )[:10]

    results1 = Pixel_B.objects.filter(
        Q(lable1__icontains=query) |
        Q(lable2__icontains=query) |
        Q(lable3__icontains=query)
    )[:10]

    results2 = Pixel_A.objects.filter(
        Q(lable1__icontains=query) |
        Q(lable2__icontains=query) |
        Q(lable3__icontains=query)
    )[:10]
    data = []
    naive_dt = datetime.now()
    current_system_time = timezone.make_aware(naive_dt, timezone.get_current_timezone())


    for i, res in enumerate([results0, results1, results2]):
        for button_item in res:
            for j in ['1','2','3']:
                new_datetime = eval('button_item.update_time' + j) + timedelta(seconds=eval('button_item.del_time' + j))
                try:
                    uu = User.objects.get(pk=eval('button_item.u' + j)).username
                except :
                    uu = None

                if current_system_time <= new_datetime:
                    if query in eval('button_item.lable' + j):
                        if i == 0:
                            data.append({'source': '社会', 'id': button_item.id, 'name': eval('button_item.lable' + j), 'is_del': 1, 'uu':uu})
                        elif i == 1:
                            data.append({'source': '电影', 'id': button_item.id, 'name': eval('button_item.lable' + j), 'is_del': 1, 'uu':uu})
                        elif i == 2:
                            data.append({'source': '游戏', 'id': button_item.id, 'name': eval('button_item.lable' + j), 'is_del': 1, 'uu':uu})
                else:
                    if query in eval('button_item.lable' + j):
                        if i == 0:
                            data.append({'source': '社会', 'id': button_item.id, 'name': eval('button_item.lable' + j), 'is_del': 0, 'uu':uu})
                        elif i == 1:
                            data.append({'source': '电影', 'id': button_item.id, 'name': eval('button_item.lable' + j), 'is_del': 0, 'uu':uu})
                        elif i == 2:
                            data.append({'source': '游戏', 'id': button_item.id, 'name': eval('button_item.lable' + j), 'is_del': 0, 'uu':uu})

    return JsonResponse(data, safe=False)


##主页
@login_required
def index(request):

    user_info = {}
    user_info['username'] = User.objects.get(username=request.user).username
    user_info['user_id'] = UserProfile.objects.get(user=request.user).user_id
    user_info['user_level'] = UserProfile.objects.get(user=request.user).user_level
    user_info['user_experience'] = UserProfile.objects.get(user=request.user).user_experience
    user_info['user_points'] = UserProfile.objects.get(user=request.user).user_points
    user_info['is_realname_authenticated'] = UserProfile.objects.get(user=request.user).is_realname_authenticated
    user_info['avatar_url'] = UserProfile.objects.get(user=request.user).avatar_url


    p_buttons_content_baiban = []
    for p_button in Pixel_W.objects.all():
        update_list, value_list, lable_list, user_list = [],[],[],[]
        update_list.append('')
        value_list.append(p_button.z1)
        lable_list.append('')
        user_list.append('')
        if hex(int(value_list[update_list.index(max(update_list))]))[2:] == 0:
            max_value = '#120202'
        else:
            max_value = '#' + hex(int(value_list[update_list.index(max(update_list))]))[2:]

        p_buttons_content_baiban.append([p_button.id, max_value, len(update_list)])

    p_buttons_content_game = []
    for p_button in Pixel_A.objects.all():
        update_list, value_list, lable_list, user_list, deltime_list = udzl(p_button)
        if hex(int(value_list[update_list.index(max(update_list))]))[2:] == 0:
            max_value = '#120202'
        else:
            max_value = '#' + hex(int(value_list[update_list.index(max(update_list))]))[2:]

        p_buttons_content_game.append([p_button.id, max_value, len(update_list)])

    p_buttons_content_dianying = []
    for p_button in Pixel_B.objects.all():
        update_list, value_list, lable_list, user_list, deltime_list = udzl(p_button)
        if hex(int(value_list[update_list.index(max(update_list))]))[2:] == 0:
            max_value = '#120202'
        else:
            max_value = '#' + hex(int(value_list[update_list.index(max(update_list))]))[2:]

        p_buttons_content_dianying.append([p_button.id, max_value, len(update_list)])

    p_buttons_content_shehui = []
    range_id = [i for i in range(10)]
    for p_button in pp.objects.all():
        update_list, value_list, lable_list, user_list, deltime_list = udzl(p_button)
        if hex(int(value_list[update_list.index(max(update_list))]))[2:] == 0:
            max_value = '#120202'
        else:
            max_value = '#' + hex(int(value_list[update_list.index(max(update_list))]))[2:]
        p_buttons_content_shehui.append([p_button.id, max_value, len(update_list)])
    searchQuery = request.POST.get('searchQuery')

    form = SearchForm(request.POST)  # 创建表单实例并填充request.GET数据
    if searchQuery == '':
        search_results = None
    else:
        search_results = pp.objects.filter(lable1=searchQuery)

    return render(request, "index.html", {"p_buttons_content_baiban": p_buttons_content_baiban,
                                          "p_buttons_content_game": p_buttons_content_game,
                                          "p_buttons_content_dianying": p_buttons_content_dianying,
                                          "p_buttons_content_shehui": p_buttons_content_shehui,
                                          "range_id": range_id,
                                          'form': form,
                                          'search_results': search_results,
                                          'user_info': user_info})

@login_required
def isFollow(request):
    if request.POST.get('followBtn_1') and request.POST.get('followBtn_2'):
        followed_user1 = get_object_or_404(User, id=request.POST.get('followBtn_1'))
        followed_user2 = get_object_or_404(User, id=request.POST.get('followBtn_2'))
        if request.POST.get('isFollowed') == '关注':
            if followed_user1 != followed_user2:
                Follow.objects.create(follower=followed_user2, followed=followed_user1)
                data = {'isFollowedflag': 0}
                return JsonResponse({'success': True, 'data': data})
        elif request.POST.get('isFollowed') == '取消关注':
            data = {'isFollowedflag': 1}
            Follow.objects.filter(follower=followed_user2, followed=followed_user1).delete()
            return JsonResponse({'success': True, 'data': data})
    return JsonResponse({'success': False, })
