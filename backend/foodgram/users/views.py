from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets

from users.models import Subscribe, User
from api.pagination import CustomPagination
from api.serializers import SubscribeSerializer, CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = CustomPagination
    serializer_class = CustomUserSerializer

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = self.request.user
        serializer = CustomUserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        if (
            isinstance(serializer, CustomUserSerializer) and
            "password" in self.request.data
        ):
            password = make_password(self.request.data["password"])
            serializer.save(password=password)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if (
            isinstance(serializer, CustomUserSerializer) and
            "password" in self.request.data
        ):
            password = make_password(self.request.data["password"])
            serializer.save(password=password)
        else:
            serializer.save()

    @action(detail=False,
            methods=['post'],
            permission_classes=[IsAuthenticated])
    def set_password(self, request):
        user = request.user
        new_password = request.data.get('new_password')

        if not new_password:
            return Response(
                {'detail': 'Пожалуйста, укажите новый пароль.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {'detail': 'Пароль успешно изменен!'},
            status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['post'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, *args, **kwargs):
        """Создание подписки."""
        author = get_object_or_404(User, id=self.kwargs.get('pk'))
        user = self.request.user
        serializer = SubscribeSerializer(
            data={'author': author.pk},
            context={'request': request, 'author': author}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response({'Подписка успешно создана': serializer.data},
                            status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, pk, **kwargs):
        """Удаление подписки."""
        author = get_object_or_404(User, id=self.kwargs.get('pk'))
        user = self.request.user
        if Subscribe.objects.filter(author=author, user=user).exists():
            Subscribe.objects.get(author=author, user=user).delete()
            return Response('Успешная отписка',
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Объект не найден'},
                        status=status.HTTP_404_NOT_FOUND)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        """Отображает все подписки пользователя."""
        follows = Subscribe.objects.filter(user=self.request.user)
        pages = self.paginate_queryset(follows)
        serializer = SubscribeSerializer(pages,
                                         many=True,
                                         context={'request': request})
        return self.get_paginated_response(serializer.data)
