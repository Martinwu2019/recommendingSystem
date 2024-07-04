import os
import json
from django.shortcuts import render, HttpResponse, reverse, redirect
from .models import *
from django.conf import settings
from django.http import FileResponse, JsonResponse
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

# 定义账号存储文件路径
json_file_path = os.path.join(r'./data/user_data.json')
# 定义用户喜欢列表文件路径
user_like_file_path = os.path.join(r'./data/user_like.json')


def index(request):
    user_name = request.session.get('username')
    data = {"user_name": user_name}
    return render(request, 'index.html', data)


def login(request):
    return render(request, 'login.html')


# 检验登录
def check_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_password')
        # 检查用户名和密码是否存在
        # 读取json文件中的数据
        with open(json_file_path, 'r') as lines:
            for line in lines:
                user_data = json.loads(line)
                if user_name == user_data.get("username") and user_password == user_data.get("password"):
                    response = redirect(reverse("APP:all_dishes"))
                    # session
                    request.session['username'] = user_name
                    request.session['username'] = user_name
                    # session过期时间（半天后）
                    request.session.set_expiry(0.5 * 24 * 3600)
                    return response
            else:
                return render(request, "login.html", {"error": True})
    else:
        return render(request, "login.html")


def register(request):
    return render(request, 'register.html')


# 检验注册
def check_register(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_password')

        # 检查用户名是否已经存在
        # 如果文件不存在，则创建一个空的json文件
        if not os.path.exists(json_file_path):
            print("文件不存在，已自动创建user_data.json文件")
            with open(json_file_path, 'w') as f:
                json.dump({}, f)
                f.write("\n")
        # 读取json文件中的数据
        with open(json_file_path, 'r') as lines:
            for line in lines:
                user_data = json.loads(line)
                if user_name == user_data.get("username"):
                    return render(request, "register.html", {"error": True})
            else:
                # 将用户数据追加到json文件
                with open(json_file_path, 'a') as file:
                    data = {'username': user_name, 'password': user_password}
                    json.dump(data, file)
                    file.write('\n')
                    return render(request, "register.html", {"succeed": True})
    else:
        return render(request, "register.html")


# 退出登录
def logout(request):
    response = redirect(reverse("APP:login"))
    # 删除cookie
    # response.delete_cookie('username')
    # 删除session(不论session中有几个值全删除，因为在数据库表django_session中所有值全在一条数据里)
    session_key = request.session.session_key
    request.session.delete(session_key)

    return response

# 所有菜肴
def all_dishes(request):
    if "username" in request.session.keys():
        user_name = request.session.get('username')
        # 读取图片名称和图片路径
        path_imgs = os.path.join(settings.BASE_DIR, 'static', 'images', '越南美食图片')
        files_name_list = []
        files_path_list = []
        for files in os.listdir(path_imgs):
            files_name_list.append(files.split(".")[0])
            files_path_list.append('../static/images/越南美食图片/' + files)
        items = zip(files_name_list, files_path_list)
        # 读取喜欢的食物文件
        like_food_list = []
        all_data = []
        # 读取json文件
        with open('./data/user_like.json', 'r') as f:
            for line in f:
                all_data.append(json.loads(line))

        for user in all_data:
            if user.get('username') == user_name:
                like_food_list = user['like_list']
        # 读取美食简介文件
        # 打开并读取JSON文件
        with open('./data/food_introduction.json', 'r') as f:
            food_introduction = json.load(f)

        Administrator = False
        if user_name == "凤梨罐头":
            Administrator = True
        data = {"user_name": user_name, "items": items, "like_food_list": like_food_list,
                "food_introduction": food_introduction, "Administrator": Administrator}
        return render(request, "all_dishes.html", data)
    else:
        return render(request, "index.html")

# 饮品类型
def food_drink(request):
    if "username" in request.session.keys():
        user_name = request.session.get('username')
        # 读取图片名称和图片路径
        files_path_list = []
        # 以读取模式打开json文件
        with open('./data/food_classify.json', 'r') as f:
            # 将文件对象转换为Python字典
            food_drink_name = json.load(f).get("drink")
        for food_name in food_drink_name:
            files_path_list.append('../static/images/越南美食图片/' + food_name + ".jpg")
        items = zip(food_drink_name, files_path_list)

        # 读取喜欢的食物文件
        like_food_list = []
        all_data = []
        # 读取json文件
        with open('./data/user_like.json', 'r') as f:
            for line in f:
                all_data.append(json.loads(line))

        for user in all_data:
            if user.get('username') == user_name:
                like_food_list = user['like_list']
        # 读取美食简介文件
        # 打开并读取JSON文件
        with open('./data/food_introduction.json', 'r') as f:
            food_introduction = json.load(f)

        data = {"user_name": user_name, "items": items, "like_food_list": like_food_list,
                "food_introduction": food_introduction}
        return render(request, "food_drink.html", data)
    else:
        return render(request, "index.html")

# 主食类型
def food_staple(request):
    if "username" in request.session.keys():
        user_name = request.session.get('username')  # 注释代码
        # 读取图片名称和图片路径
        files_path_list = []
        # 以读取模式打开json文件
        with open('./data/food_classify.json', 'r') as f:
            # 将文件对象转换为Python字典
            food_drink_name = json.load(f).get("staple")
        for food_name in food_drink_name:
            files_path_list.append('../static/images/越南美食图片/' + food_name + ".jpg")
        items = zip(food_drink_name, files_path_list)

        # 读取喜欢的食物文件
        like_food_list = []
        all_data = []
        # 读取json文件
        with open('./data/user_like.json', 'r') as f:
            for line in f:
                all_data.append(json.loads(line))

        for user in all_data:
            if user.get('username') == user_name:
                like_food_list = user['like_list']
        # 读取美食简介文件
        # 打开并读取JSON文件
        with open('./data/food_introduction.json', 'r') as f:
            food_introduction = json.load(f)

        data = {"user_name": user_name, "items": items, "like_food_list": like_food_list,
                "food_introduction": food_introduction}
        return render(request, "food_staple.html", data)
    else:
        return render(request, "index.html")

# 菜品类型
def food_dishes(request):
    if "username" in request.session.keys():
        user_name = request.session.get('username')
        # 读取图片名称和图片路径
        files_path_list = []
        # 以读取模式打开json文件
        with open('./data/food_classify.json', 'r') as f:
            # 将文件对象转换为Python字典
            food_drink_name = json.load(f).get("dishes")
        for food_name in food_drink_name:
            files_path_list.append('../static/images/越南美食图片/' + food_name + ".jpg")
        items = zip(food_drink_name, files_path_list)

        # 读取喜欢的食物文件
        like_food_list = []
        all_data = []
        # 读取json文件
        with open('./data/user_like.json', 'r') as f:
            for line in f:
                all_data.append(json.loads(line))

        for user in all_data:
            if user.get('username') == user_name:
                like_food_list = user['like_list']
        # 读取美食简介文件
        # 打开并读取JSON文件
        with open('./data/food_introduction.json', 'r') as f:
            food_introduction = json.load(f)

        data = {"user_name": user_name, "items": items, "like_food_list": like_food_list,
                "food_introduction": food_introduction}
        return render(request, "food_dishes.html", data)
    else:
        return render(request, "index.html")

# 甜点类型
def food_dessert(request):
    if "username" in request.session.keys():
        user_name = request.session.get('username')
        # 读取图片名称和图片路径
        files_path_list = []
        # 以读取模式打开json文件
        with open('./data/food_classify.json', 'r') as f:
            # 将文件对象转换为Python字典
            food_drink_name = json.load(f).get("dessert")
        for food_name in food_drink_name:
            files_path_list.append('../static/images/越南美食图片/' + food_name + ".jpg")
        items = zip(food_drink_name, files_path_list)

        # 读取喜欢的食物文件
        like_food_list = []
        all_data = []
        # 读取json文件
        with open('./data/user_like.json', 'r') as f:
            for line in f:
                all_data.append(json.loads(line))

        for user in all_data:
            if user.get('username') == user_name:
                like_food_list = user['like_list']
        # 读取美食简介文件
        # 打开并读取JSON文件
        with open('./data/food_introduction.json', 'r') as f:
            food_introduction = json.load(f)

        data = {"user_name": user_name, "items": items, "like_food_list": like_food_list,
                "food_introduction": food_introduction}
        return render(request, "food_dessert.html", data)
    else:
        return render(request, "index.html")

# 数据可视化
def data_visualization(request):
    if "username" in request.session.keys():
        user_name = request.session.get('username')
        # 初始化字典
        ranking_dist = {}
        food_type_like = {}
        try:
            # 读取user_like.json文件
            with open('./data/user_like.json', 'r') as f:
                for line in f:
                    if json.loads(line).get("like_list"):
                        for food in json.loads(line).get("like_list"):
                            # 如果元素在字典中存在，其值加1
                            if food in ranking_dist.keys():
                                ranking_dist[food] += 1
                            # 如果元素在字典中不存在，将其加入字典，值为1
                            else:
                                ranking_dist[food] = 1
            print(ranking_dist)
            # 以读取模式打开food_classify.json文件
            with open('./data/food_classify.json', 'r') as f:
                # 将文件对象转换为Python字典
                food_classify = json.load(f)
            # 检测用户喜欢那种类型的美食
            for food_name in ranking_dist.keys():
                for food_type, type_food in food_classify.items():
                    # 检测到食物所属类型并且字典中存在该食物类型
                    if (food_name in type_food):
                        if (food_type in food_type_like.keys()):
                            food_type_like[food_type] += 1
                        # 如果元素在字典中不存在，将其加入字典，值为1
                        else:
                            food_type_like[food_type] = 1
            print(food_type_like)
        except Exception as e:
            print("出现错误", e)

        # 将食物类型喜欢字典中的英文类型名称转为中文
        food_type_like = {"饮品": food_type_like.get("drink"), "主食": food_type_like.get("staple"), "菜品":
            food_type_like.get("dishes"), "甜点": food_type_like.get("dessert")}
        data = {"user_name": user_name, "ranking_dist": ranking_dist, "food_type_like": food_type_like}
        print(food_type_like)
        return render(request, "data_visualization.html", data)
    else:
        return render(request, "index.html")

# 猜你喜欢
def guess_youlike(request):
    if "username" in request.session.keys():
        user_name = request.session.get('username')
        try:
            like_food_data = []
            # 读取json文件
            with open('./data/user_like.json', 'r') as f:
                for line in f:
                    like_food_data.append(json.loads(line))
        except Exception as e:
            print("出现错误", e)
        # 协同过滤算法进行美食推荐
        # 用户的美食列表
        user_data = like_food_data[1:]
        print(user_data)
        # 建立美食到用户的倒排表
        food_users = defaultdict(list)
        for data in user_data:
            if data.get("like_list"):
                for food in data.get("like_list"):
                    food_users[food].append(data["username"])   # key: food; value: username[]
        print(food_users)
        # 计算用户之间的共享美食数
        user_similarity = defaultdict(int)
        for users in food_users.values():
            for user in users:
                # if user != '我':
                if user != user_name:
                    user_similarity[user] += 1      # key: user; value: similarity
        print(user_similarity)
        # 找到与“我”最相似的用户
        most_similar_user = max(user_similarity, key=user_similarity.get)
        print(most_similar_user)

        # 找到最相似用户喜欢的食物列表
        most_similar_user_foods = next(data["like_list"] for data in user_data if data["username"] == most_similar_user)
        print(most_similar_user_foods)
        # 找到“我”喜欢的食物列表
        try:
            my_foods = next(data["like_list"] for data in user_data if data["username"] == user_name)
        except:
            print("该用户未喜欢过任何美食")
            recommended_foods = []
        else:
            # 推荐最相似用户喜欢的，但“我”还未尝试过的美食
            recommended_foods = set(most_similar_user_foods) - set(my_foods)
            recommended_foods = list(recommended_foods)
            print(recommended_foods)
        files_path_list = []
        for recommended_food in recommended_foods:
            files_path_list.append('../static/images/越南美食图片/' + recommended_food + ".jpg")

        items = zip(recommended_foods, files_path_list)

        print(f"推荐的美食: {recommended_foods}")

        data = {"user_name": user_name, "items": items}
        return render(request, "guess_youlike.html", data)
    else:
        return render(request, "index.html")

# user_like.json文件操作
def like(request, food_name, operate):
    # 接收被点赞的美食名称和用户的操作，即 food_name 参数和operate参数
    user_name = request.session.get("username")
    if operate == "点赞":
        print(f"{user_name} 对 {food_name} 进行 {operate} 操作")
        # 写入文件
        # 如果文件不存在，则创建一个空的json文件
        if not os.path.exists(user_like_file_path):
            print("user_like.json文件不存在，已自动创建user_like.json文件")
            with open(user_like_file_path, 'w') as f:
                json.dump({}, f)
                f.write("\n")
        data = []
        # 读取json文件
        with open('./data/user_like.json', 'r') as f:
            for line in f:
                data.append(json.loads(line))

        # 检查用户是否存在
        user_exists = False
        for user in data:
            if user.get('username') == user_name:
                user_exists = True
                print("用户存在，检测用户之前是否喜欢过该美食")
                if food_name not in user.get('like_list'):
                    print(f"成功添加美食{food_name}")
                    # 将美食名称添加到用户的like_list
                    user['like_list'].append(food_name)
                    break

        if not user_exists:
            # 如果用户不存在，创建一个新用户
            print("创建新用户")
            data.append({'username': user_name, 'like_list': [food_name]})

        # 将更新后的数据写回json文件
        with open('./data/user_like.json', 'w') as f:
            for user in data:
                f.write(json.dumps(user, ensure_ascii=False) + '\n')
    else:
        print(f"{user_name} 对 {food_name} 进行 {operate} 操作")
        # 从文件中删除
        data = []
        # 读取json文件
        with open('./data/user_like.json', 'r') as f:
            for line in f:
                data.append(json.loads(line))
            for user in data:
                if user.get('username') == user_name:
                    # 将美食名称从like_list中移除
                    try:
                        user['like_list'].remove(food_name)
                    except Exception as e:
                        print("发生了一个错误：", e)
                    else:
                        break

                # 将更新后的数据写回json文件
            with open('./data/user_like.json', 'w') as f:
                for user in data:
                    f.write(json.dumps(user, ensure_ascii=False) + '\n')
    # 返回一个空的 HttpResponse 对象
    return HttpResponse()

# 搜索
@csrf_exempt
def search(request):
    if request.method == 'POST':
        pageUrl = request.POST.get("pageUrl").split("/")[-2]
        print(f"查询的页面是{pageUrl}")
        search_results = request.POST.get("keyword")
        print(f"查询：{search_results}")
        # 根据搜索所在的页面不同选择不同的数据库
        food_all_name = []
        # all_dishes
        if pageUrl == "all_dishes":
            # 读取所有美食的名字
            path_imgs = os.path.join(settings.BASE_DIR, 'static', 'images', '越南美食图片')

            for files in os.listdir(path_imgs):
                food_all_name.append(files.split(".")[0])
        else:
            # 菜品子属性直接从food_classify.json读取出字典调用对应键
            # 以读取模式打开json文件
            with open('./data/food_classify.json', 'r') as f:
                # 将文件对象转换为Python字典
                food_all_name = json.load(f).get(pageUrl.split("_")[-1])

        # 模糊查询
        search_food = []
        for name in food_all_name:
            if (search_results in name) and (name not in search_food):
                search_food.append(name)
        print(f"查询结果：{search_food}")
        # 将结果返回给前端
        # return JsonResponse({'data': search_food})

        # 将查询到的美食名称列表返回前端
        return JsonResponse({'redirect': '/food_single/', 'arg': search_food})

# 搜索
def food_single(request):
    search_food = request.GET.get('arg', '')
    user_name = request.session.get("username")

    # 可能传过来一个或多个食物
    if ',' in search_food:
        search_food = search_food.split(',')
    else:
        search_food = [search_food]

    # 读取喜欢的食物文件
    like_food_list = []
    all_data = []
    # 读取json文件
    with open('./data/user_like.json', 'r') as f:
        for line in f:
            all_data.append(json.loads(line))

    for user in all_data:
        if user.get('username') == user_name:
            like_food_list = user['like_list']

    # 读取所有美食的名字
    path_imgs = os.path.join(settings.BASE_DIR, 'static', 'images', '越南美食图片')
    food_all_name = []
    for files in os.listdir(path_imgs):
        food_all_name.append(files.split(".")[0])

    for food in search_food:
        # 如果搜索的名称存在于美食数据库中
        if food in food_all_name:
            # 美食名称和路径
            files_path_list = []
            for food_name in search_food:
                files_path_list.append('../static/images/越南美食图片/' + food_name + ".jpg")
            items = zip(search_food, files_path_list)
            # 读取美食简介文件
            # 打开并读取JSON文件
            with open('./data/food_introduction.json', 'r') as f:
                food_introduction = json.load(f)

            data = {"items": items, "food_introduction": food_introduction, "like_food_list": like_food_list}
            return render(request, "food_single.html", data)
    else:
        return HttpResponse("没有找到任何相关美食")

# 当前用户的所有喜欢的菜
def all_user(request):
    if "username" in request.session.keys():
        user_name = request.session.get("username")
        # 读取喜欢的食物文件
        like_food_list = []
        like_food_path = []
        all_data = []
        # 读取json文件
        with open('./data/user_like.json', 'r') as f:
            for line in f:
                all_data.append(json.loads(line))

        for user in all_data:
            if user.get('username') == user_name:
                like_food_list = user['like_list']
        # 图片路径
        for food_name in like_food_list:
            like_food_path.append('../static/images/越南美食图片/' + food_name + ".jpg")

        # 读取美食简介文件
        # 打开并读取JSON文件
        with open('./data/food_introduction.json', 'r') as f:
            food_introduction = json.load(f)
            print(food_introduction)

        items = zip(like_food_list, like_food_path)
        data = {"user_name": user_name, "items": items, "food_introduction": food_introduction,
                "like_food_list": like_food_list}
        return render(request, "all_user.html", data)
    else:
        return render(request, "index.html")


def add_image(request):
    return render(request, "add_image.html")


@csrf_exempt
def receive_image(request):
    if request.method == 'POST':
        # 获取上传的图片
        img = request.FILES.get('img')
        # 检查是否有图片被上传
        if img is None:
            return HttpResponse('请上传一张图片')
        # 获取菜品名称
        food_name = request.POST.get('food_name')

        # 创建一个文件系统存储对象，并指定保存文件的路径
        path_imgs = os.path.join(settings.BASE_DIR, 'static', 'images', '越南美食图片')
        fs = FileSystemStorage(location=path_imgs)
        # 以美食名称为文件名保存图片
        filename = fs.save(food_name + '.jpg', img)

        # 获取菜品种类
        categories = request.POST.getlist('category')
        if len(categories) >= 1:
            # 打开JSON文件
            with open('./data/food_classify.json', 'r') as f:
                # 加载JSON文件中的数据
                food_type = json.load(f)
            # 将美食类型写入文件
            for categorie in categories:
                food_type[categorie].append(food_name)
            # 将字典保存回JSON文件
            with open('./data/food_classify.json', 'w') as f:
                json.dump(food_type, f)

        # 获取简介
        intro = request.POST.get('intro')
        if len(intro) >= 1:
            # 打开JSON文件
            with open('./data/food_introduction.json', 'r') as f:
                # 加载JSON文件中的数据
                food_introduction = json.load(f)
            # 将简介写入文件
            food_introduction[food_name] = intro
            # 将字典保存回JSON文件
            with open('./data/food_introduction.json', 'w') as f:
                json.dump(food_introduction, f)

        # return HttpResponse(f"{food_name}上传成功")
        return HttpResponse(f'<a href="javascript:history.back();">{food_name}上传成功，点击返回主页</a>')
    else:
        return HttpResponse("上传失败")
