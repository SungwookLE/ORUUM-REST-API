#  file: backend/settings/base.py

from pathlib import Path
import os

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'api.apps.ApiConfig',
    'accounts.apps.AccountsConfig',
    'dashboard.apps.DashboardConfig',

    # REST Framework
    'rest_framework',
    # drf_yasg: django rest framework- Yet another Swagger generator
    'drf_yasg',
    
    # ========================================
    # CORS: Crosss-Origin Resource Sharing)
    # 웹 페이지 상의 제한된 리소스를 최초 자원이 서비스된 도메인(REST API) 밖의 다른 도메인(FRONT)으로부터 요청할 수 있게 허용하는 구조
    'corsheaders',
    # ========================================

    # ========================================
    # 카카오톡 소셜 로그인 관련 부분
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # provider setting
    'allauth.socialaccount.providers.kakao',
    # ========================================

    # ========================================
    # dash, plottly
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    # ========================================
]

# ========================================
# 카카오 소셜 로그인을 위한 세팅 환경 변수 선언
SITE_ID = 1
LOGIN_REDIRECT_URL = 'home'  # 로그인 후 리다이렉트 될 경로
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True  # 로그아웃 버튼 클릭 시 자동 로그아웃
SOCIALACCOUNT_AUTO_SIGNUP = False
ACCOUNT_SIGNUP_FORM_CLASS = 'accounts.forms.SignupForm'
# ========================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

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

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of 'allauth'
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth' specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/')]
#STATICFILES_DIRS = [BASE_DIR / 'static',]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========================================
# CORS 설정
# CORS_ORIGIN_ALLOW_ALL: If True, all origins will be accepted (not use the whitelist below). Defaults to False.
# CORS_ORIGIN_WHITELIST: List of origins that are authorized to make cross-site HTTP requests. Defaults to [].
CORS_ORIGIN_WHITELIST = ['http://3.37.170.52', 'http://localhost:8000']
CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = ['http://3.37.170.52', "https://api.oruum.com", "http://0.0.0.0:8000"]
# ========================================

# ========================================
# 장고의 default 유저 모델인 abstractUser를 상속시켜 만든 커스텀 모델을 default 모델로 사용을 원할 경우, 모델을 지정해주어야 함
AUTH_USER_MODEL = 'accounts.UserList'
# ========================================

# ========================================
# plotly dash
X_FRAME_OPTIONS = 'SAMEORIGIN'
# ========================================
