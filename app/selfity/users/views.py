from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import OrderingFilter as DjangoOrderingFilter
from .models import User, Post
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer,\
    CreatePhoneSesionSerializer, CreateSesionSerializer,\
    UserValidateTokenSerializer, PostSerializer, PostRetieveSerializer,\
    PostListSerializer, PostHashtagSerializer
from selfity.users.utils import CustomValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class UserPhoneCreateViewSet(mixins.CreateModelMixin,
                                viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreatePhoneSesionSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        try:
            return super(UserPhoneCreateViewSet, self).create(request,
                                                              *args,
                                                              **kwargs)
        except CustomValidationError as e:
            return Response(status=e.status_code, data=e.detail)


class UserPhoneCreateSesionViewSet(mixins.CreateModelMixin,
                                   viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateSesionSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            refresh = RefreshToken.for_user(user)
            return Response(status=200, data={
                'token': str(
                    refresh.access_token),
            })
        else:
            return Response(data=serializer.errors, status=400)


class UserValidateTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserValidateTokenSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        JWT_authenticator = JWTAuthentication()
        JWT_authenticator.get_validated_token(request.data.get('token'))
        return Response()


class PostCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny, )


class PostRetrieveViewSet(mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostRetieveSerializer
    permission_classes = (AllowAny, )


class OrderingFilter(DjangoOrderingFilter):
    def get_valid_fields(self, queryset, view, context={}):
        valid_fields = getattr(view, 'ordering_fields', self.ordering_fields)
        if isinstance(valid_fields, dict):
            return valid_fields.items()
        else:
            return super(OrderingFilter, self).get_valid_fields(
                queryset,
                view,
                context
            )

    def get_ordering(self, request, queryset, view):
        valid_fields = getattr(view, 'ordering_fields', self.ordering_fields)
        if isinstance(valid_fields, dict):
            params = request.query_params.get(self.ordering_param)

            if params:
                fields = [param.strip() for param in params.split(',')]
                _ordering = self.remove_invalid_fields(
                    queryset,
                    fields,
                    view,
                    request
                )

                ordering = []
                for item in _ordering:
                    if '-' in item:
                        ordering.append(
                            '-{}'.format(valid_fields.get(item[1:]))
                        )
                    else:
                        ordering.append(
                            valid_fields.get(item)
                        )
                if ordering:
                    return ordering
            return self.get_default_ordering(view)
        else:
            return super(OrderingFilter, self).get_ordering(
                request,
                queryset,
                view
            )


class PostListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = (AllowAny, )
    filter_backends = (OrderingFilter,)
    ordering_fields = {'created': "created_at",
                       'id': 'id'}



class PostHashtagListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostHashtagSerializer
    permission_classes = (AllowAny, )