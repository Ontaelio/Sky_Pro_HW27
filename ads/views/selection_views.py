from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from ads.models import Selection
from ads.serializers import SelectionListSerializer, SelectionCreateSerializer, SelectionDetailSerializer, \
    SelectionUpdateSerializer, SelectionDeleteSerializer


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    

class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionUpdateSerializer


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDeleteSerializer
