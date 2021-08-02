from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from selfity.curp.serializers import CurpSerializer
from selfity.curp.utils import Bot


class CurpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CurpSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(request)
        if serializer.is_valid():
            bot = Bot()
            bot.get_web()
            curp = bot.get_curp()
            return Response(data={"data": curp})
