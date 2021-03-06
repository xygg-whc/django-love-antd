import json
from django_filters import rest_framework
from antd_pro.common.pagination import AntdPageNumberPagination
from rest_framework.parsers import JSONParser
from antd_pro.models import AntdPermission, AntdRole, AntdUser, AntdUserProfile, AntdCasbinRule, AntdMenuRule
from .common.parsers import MultipartJsonParser
import os
from django.conf import settings
from django.apps import apps
from .filters import AntdCasbinFilter, AntdRoleFilter, AntdUserFilter, AntdMenuRuleFilter
from .serializers import AntdPermissionSerializer, AntdPermissionFormSerializer, AntdRoleSerializer, \
    AntdRoleFormSerializer, AntdUserSerializer, AntdUserFormSerializer, LoginSerializer, AntdCasbinRuleSerializer, \
    AntdCasbinRuleFormSerializer, AntdCasbinBatchDeleteSerializer, AntdUserBatchDeleteSerializer, \
    AntdRoleBatchDeleteSerializer, AntdPermissionBatchDeleteSerializer, AntdMenuSerializer, AntdMenuFormSerializer, \
    AntdMenuBatchDeleteSerializer
from antd_pro.common.response.renderer import Renderer
from antd_pro.common.response.response import DataPackage, JsonResponse
from antd_pro.utils.hashers import make_jwt
from antd_pro.common.viewsets import ModelViewSet
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework import filters
from django.db import transaction
from rest_framework import status
from antd_pro.common.authentication import TokenAuthentication
from antd_pro.common.permission import CasbinAccessPermission


class AntdPermissionViewSet(ModelViewSet):
    serializer_class = AntdPermissionSerializer
    queryset = AntdPermission.objects.filter()
    renderer_classes = (Renderer,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', 'name')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CasbinAccessPermission,)
    pagination_class = AntdPageNumberPagination

    def list(self, request, *args, **kwargs):
        """
        ๆ้ๅ่กจ
        """
        return super(AntdPermissionViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        ๆ้่ฏฆๆ
        """
        return super(AntdPermissionViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        ๆดๆฐๆ้
        """
        self.serializer_class = AntdPermissionFormSerializer
        return super(AntdPermissionViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        ๅ?้คๆ้
        """
        return super(AntdPermissionViewSet, self).destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        ๅๅปบๆ้
        """
        self.serializer_class = AntdPermissionFormSerializer
        return super(AntdPermissionViewSet, self).create(request, *args, **kwargs)

    def batch_destory(self, request, *args, **kwargs):
        """
        ๆน้ๅ?้ค
        """
        data = request.data
        ids = data.get('ids')
        ser = AntdPermissionBatchDeleteSerializer(data=ids, many=True)
        ser.is_valid()
        self.queryset = self.queryset.filter(id__in=ids).delete()
        return JsonResponse(msg='ๅ?้คๆๅ')


class AntdRoleViewSet(ModelViewSet):
    serializer_class = AntdRoleSerializer
    queryset = AntdRole.objects.filter().order_by('id')
    renderer_classes = (Renderer,)
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    pagination_class = AntdPageNumberPagination
    filterset_class = AntdRoleFilter

    def list(self, request, *args, **kwargs):
        """
        ่ง่ฒๅ่กจ
        """
        return super(AntdRoleViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        ่ง่ฒ่ฏฆๆ
        """
        return super(AntdRoleViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        ๆดๆฐ่ง่ฒ
        """
        self.serializer_class = AntdRoleFormSerializer
        return super(AntdRoleViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        ๅ?้ค่ง่ฒ
        """
        return super(AntdRoleViewSet, self).destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        ๅๅปบ่ง่ฒ
        """
        self.serializer_class = AntdRoleFormSerializer
        return super(AntdRoleViewSet, self).create(request, *args, **kwargs)

    def batch_destory(self, request, *args, **kwargs):
        """
        ๆน้ๅ?้ค
        """
        data = request.data
        ids = data.get('ids')
        ser = AntdRoleBatchDeleteSerializer(data=ids, many=True)
        ser.is_valid()
        self.queryset = self.queryset.filter(id__in=ids).delete()
        return JsonResponse(msg='ๅ?้คๆๅ')


class AntdUserViewSet(ModelViewSet):
    serializer_class = AntdUserSerializer
    queryset = AntdUser.objects.filter().order_by('id')
    renderer_classes = (Renderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CasbinAccessPermission,)
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    pagination_class = AntdPageNumberPagination
    filterset_class = AntdUserFilter

    def list(self, request, *args, **kwargs):
        """
        ็จๆทๅ่กจ
        """
        return super(AntdUserViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        ็จๆท่ฏฆๆ
        """
        return super(AntdUserViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        ๆดๆฐ็จๆท
        """
        data = request.data
        ser = AntdUserFormSerializer(data=data)
        ser.is_valid()
        with transaction.atomic():
            user_qs = AntdUser.objects.filter(id=data.get('id'))
            user_qs.update(phone_num=data.get('phoneNum'),
                           is_super=bool(data.get('is_super')))
            user = user_qs.first()
            roles = AntdRole.objects.filter(id__in=data.get('roles', []))
            user.roles.set(roles)
            profile_qs = AntdUserProfile.objects.filter(user=user).first()
            profile_qs.birthday = data.get('profile__birthday')
            profile_qs.gender = data.get('profile__gender')
            if data.get('profile__avatar'):
                profile_qs.avatar = data.get('profile__avatar')
            profile_qs.email = data.get('profile__email')
            profile_qs.save()
            ser = AntdUserSerializer(instance=user)
            _d = DataPackage().set_fields(ser.data)
            return JsonResponse(data=_d, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        return super(AntdUserViewSet, self).destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        ๅๅปบ็จๆท
        """
        data = request.data
        ser = AntdUserFormSerializer(data=data)
        ser.is_valid()
        with transaction.atomic():
            user = AntdUser(phone_num=data.get('phoneNum'), is_super=bool(data.get('is_super')))
            user.password = make_password(data.get('password'))
            roles = AntdRole.objects.filter(id__in=data.get('roles', []))
            user.save()
            user.roles.set(roles)
            profile = AntdUserProfile(birthday=data.get('profile__birthday'), gender=data.get('profile__gender'),
                                      avatar=data.get('profile__avatar'), email=data.get('profile__email'), user=user)
            profile.save()
            ser = AntdUserSerializer(instance=user)
            _d = DataPackage().set_fields(ser.data)
            return JsonResponse(data=_d, status=status.HTTP_201_CREATED)

    def batch_destory(self, request, *args, **kwargs):
        """
        ๆน้ๅ?้ค
        """
        data = request.data
        ids = data.get('ids')
        ser = AntdUserBatchDeleteSerializer(data=ids, many=True)
        ser.is_valid()
        self.queryset = self.queryset.filter(id__in=ids).delete()
        return JsonResponse(msg='ๅ?้คๆๅ')


class LoginViewSet(ModelViewSet):
    serializer_class = LoginSerializer
    renderer_classes = (Renderer,)

    def login(self, request, *args, **kwargs):
        """
        ็ป้
        """
        data = request.data
        ser = LoginSerializer(data=data)
        ser.is_valid(raise_exception=True)
        phone_num = data.get('phoneNum')
        user = AntdUser.objects.filter(phone_num=phone_num).first()
        ser = AntdUserSerializer(instance=user)
        userinfo = ser.data
        token = make_jwt(userinfo)
        _d = DataPackage().set_fields(userinfo).set_field('token', token)

        return JsonResponse(data=_d)

    @authentication_classes(authentication_classes=(TokenAuthentication,))
    def current_user(self, request, *args, **kwargs):
        """
        ็จๆท่ฏฆๆ
        """
        user = request.user
        ser = AntdUserSerializer(instance=user)
        _d = DataPackage().set_fields(ser.data)
        return JsonResponse(data=_d)


class AntdCasbinRuleViewSet(ModelViewSet):
    serializer_class = AntdCasbinRuleSerializer
    queryset = AntdCasbinRule.objects.filter().order_by('id')
    renderer_classes = (Renderer,)
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    pagination_class = AntdPageNumberPagination
    filterset_class = AntdCasbinFilter

    # filterset_fields = ('v1',)

    def list(self, request, *args, **kwargs):
        return super(AntdCasbinRuleViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = AntdCasbinRuleFormSerializer
        data = request.data
        ser = AntdCasbinRuleFormSerializer(data=data)
        ser.is_valid()
        # ๅๆฐ1๏ผ่ง่ฒ้ๅ๏ผr.sub in p.sub
        # ๅๆฐ2, ่ตๆบๅฐๅ, r.obj == p.obj
        # ๅๆฐ3๏ผ่ฏทๆฑๆนๆณ๏ผr.act == p.act
        rule = AntdCasbinRule(ptype='p')
        rule.v0 = json.dumps(data.get('roles', []))
        rule.v1 = data.get('route')
        rule.v2 = data.get('method')
        rule.save()
        ser = AntdCasbinRuleSerializer(instance=rule)
        _d = DataPackage(rc=status.HTTP_201_CREATED).set_fields(ser.data)
        return JsonResponse(data=_d, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        return super(AntdCasbinRuleViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = AntdCasbinRuleFormSerializer
        data = request.data
        ser = AntdCasbinRuleFormSerializer(data=data)
        ser.is_valid()
        # ๅๆฐ1๏ผ่ง่ฒ้ๅ๏ผr.sub in p.sub
        # ๅๆฐ2, ่ตๆบๅฐๅ, r.obj == p.obj
        # ๅๆฐ3๏ผ่ฏทๆฑๆนๆณ๏ผr.act == p.act
        rule = AntdCasbinRule.objects.filter(ptype='p', id=data.get('id')).first()
        rule.v0 = json.dumps(data.get('roles', []))
        rule.v1 = data.get('route')
        rule.v2 = data.get('method')
        rule.save()
        ser = AntdCasbinRuleSerializer(instance=rule)
        _d = DataPackage(rc=status.HTTP_200_OK).set_fields(ser.data)
        return JsonResponse(data=_d, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return super(AntdCasbinRuleViewSet, self).destroy(request, *args, **kwargs)

    def batch_destory(self, request, *args, **kwargs):
        """
        ๆน้ๅ?้ค
        """
        data = request.data
        ids = data.get('ids')
        ser = AntdCasbinBatchDeleteSerializer(data=ids, many=True)
        ser.is_valid()
        self.queryset = self.queryset.filter(id__in=ids).delete()
        return JsonResponse(msg='ๅ?้คๆๅ')


class AntdMenuRuleViewSet(ModelViewSet):
    serializer_class = AntdMenuSerializer
    queryset = AntdMenuRule.objects.filter().order_by('id')
    renderer_classes = (Renderer,)
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    pagination_class = AntdPageNumberPagination
    filterset_class = AntdMenuRuleFilter

    def list(self, request, *args, **kwargs):
        return super(AntdMenuRuleViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = AntdMenuFormSerializer
        return super(AntdMenuRuleViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = AntdMenuFormSerializer
        return super(AntdMenuRuleViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(AntdMenuRuleViewSet, self).destroy(request, *args, **kwargs)

    def batch_destory(self, request, *args, **kwargs):
        """
        ๆน้ๅ?้ค
        """
        data = request.data
        ids = data.get('ids')
        ser = AntdMenuBatchDeleteSerializer(data=ids, many=True)
        ser.is_valid()
        self.queryset = self.queryset.filter(id__in=ids).delete()
        return JsonResponse(msg='ๅ?้คๆๅ')

    def fetch_routes(self, request, *args, **kwargs):
        """
        ๅ็ซฏ่ทฏ็ฑ
        """
        app = apps.get_app_config('antd_pro')
        with open(os.path.join(app.path, 'resources', 'routes.json'), 'r') as f:
            routes = json.loads(f.read())

        # ่ฏป่ๅ่กจ๏ผ้็ฝฎๆ้
        _d = DataPackage().set_elements(routes)
        return JsonResponse(data=_d)
