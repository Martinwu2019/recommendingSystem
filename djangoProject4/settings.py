from pathlib import Path
import os

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 项目的密钥
SECRET_KEY = 'django-insecure-5=29)8hk(l!=++teqgc#o5e@ixh54$*sf$7#k0m#ceb3b(rho)'

# 调试模式
DEBUG = True

"""当使用IP"0.0.0.0"启动项目时，系统会搜索本列表中的可用IP（在哪个网络下哪个IP就可用），
进入网站的url就是该IP + 端口号 + 路径,    * ：表示通配符，匹配所有的IP
"""
ALLOWED_HOSTS = ["*"]


# 定义应用（Django的内部应用）
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 定义自己的应用
    'APP',
]

# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 跟路由文件
ROOT_URLCONF = 'djangoProject4.urls'

# 模版
TEMPLATES = [
    # 添加jinja2模版（需要将Settings中Languages & Frameworks中的Template Languages中语言设置为jinja2）
    # {
    #     'BACKEND': 'django.template.backends.jinja2.Jinja2',
    #     # 可以存放多个templates的路径，如果view.py中调用的html文件在多个templates中都存在，
    #     # 则优先调用列表中靠前的templates中的html
    #     'DIRS': [BASE_DIR / 'templates']
    #     ,
    #     'APP_DIRS': True,
    #     # 这里要添加environment，并指定到jinja2_env文件中的environment
    #     'OPTIONS': {
    #         'environment': 'djangoProject4.jinja2_env.environment',
    #         'context_processors': [
    #             'django.template.context_processors.debug',
    #             'django.template.context_processors.request',
    #             'django.contrib.auth.context_processors.auth',
    #             'django.contrib.messages.context_processors.messages',
    #         ],
    #     },
    # },
    # 原来自带的Django模版引擎
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 可以存放多个templates的路径，如果view.py中调用的html文件在多个templates中都存在，
        # 则优先调用列表中靠前的templates中的html
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# wsgi目录
WSGI_APPLICATION = 'djangoProject4.wsgi.application'


# Database
DATABASES = {
    # SQLite
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

    # Mysql
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'db2',        # 数据库名字
    #     'USER': 'root',            # 数据库的用户名
    #     'PASSWORD': '456288',  # 数据库的密码
    #     'HOST': 'localhost',        # 这是数据库的地址"localhost"是表示默认本机的
    #     'PORT': '3306'              # 默认端口号是3306
    #     }
}


# 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 国际化
# en-us：英语，zh-hans：中文（后台管理页面的语言）
LANGUAGE_CODE = 'zh-hans'
# 时区（时间）
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# 静态文件 Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
# 配置静态文件夹
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
