from . import models
from . import serializers as app_serializers
from rest_framework import mixins, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import Group, Permission
from base.permissions_mixins import IsAdminUser, IsSuperUser, PermsApi


class PermissionViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Permission.objects.all()
    serializer_class = app_serializers.PermissionSerializer
    permission_classes = [PermsApi]

    def get_serializer_class(self):
        if self.action in ['contenttype']:
            return app_serializers.PermissionContentTypeSerializer
        return self.serializer_class

    @action(detail=True)
    def contenttype(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = app_serializers.GroupSerializer
    permission_classes = [PermsApi]

    def get_serializer_class(self):
        if self.action in ['permissions']:
            return app_serializers.GroupPermissionsSerializer
        return self.serializer_class

    @action(detail=True)
    def permissions(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class UserGlobalViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = app_serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False)
    def authenticated_user(self, request,  methods=['get']):
        obj = request.user
        serializer = app_serializers.UserFullSerializer(obj)
        return Response(serializer.data)

    @action(detail=False)
    def apps(self, request):
        from django.contrib.admin.sites import all_sites
        apps = []
        for site in all_sites:
            apps = site.get_app_list(request)
        return Response(apps, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = app_serializers.UserSerializer
    permission_classes = [PermsApi]

    def get_queryset(self):
        return super().get_queryset()

    def get_permissions(self):
        if self.action in ['set_admin']:
            self.permission_classes += [IsAdminUser]

        if self.action in ['simpleusers']:
            self.permission_classes = []
            self.serializer_class = app_serializers.UserSimpleSerializer

        if self.action in ['set_super']:
            self.permission_classes += [IsSuperUser]

        return super().get_permissions()

    @action(detail=True)
    def full(self, request, pk=None):
        obj = self.get_object()
        serializer = app_serializers.UserFullSerializer(obj)
        return Response(serializer.data)

    @action(detail=False)
    def simpleusers(self, request):
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)

    def list(self, request):
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = app_serializers.PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.updated_by = request.user
            user.save()
            return Response({'status': 'password was redefined'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def revoke_token(self, request, pk=None):
        user = self.get_object()
        serializer = app_serializers.TokenSerializer(data=request.data)
        if serializer.is_valid():
            if user.token == (serializer.validated_data['token']):
                user.token = None
                user.save()
                return Response({'status': 'token was revoked'})
            else:
                return Response({'status': 'token not found'},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def generate_token(self, request, pk=None):
        user = self.get_object()
        if not user.token:
            user.token = user.generate_token()
            user.save()
            return Response(
                {
                    'status': 'token was generated',
                    'token': user.token
                }, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'token exists'},
                            status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def set_admin(self, request, pk=None):
        if not request.user.is_superuser:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        user = self.get_object()
        serializer = app_serializers.UserAdminSerializer(data=request.data)
        if serializer.is_valid():
            user.is_staff = serializer.validated_data.get('is_staff',
                                                          user.is_staff)
            user.is_active = serializer.validated_data.get('is_active',
                                                           user.is_active)
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def set_super(self, request, pk=None):
        if not request.user.is_superuser:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        user = self.get_object()
        serializer = app_serializers.UserSuperSerializer(data=request.data)
        if serializer.is_valid():
            user.is_superuser = serializer.validated_data.get(
                'is_superuser', user.is_superuser)
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
