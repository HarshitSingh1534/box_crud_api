# Create your views here.
from rest_framework import status, generics, viewsets

from boxes.serializers import BoxSerializer
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from boxes.filters import BoxFilter, BoxUsernameDateFilter
from boxes.permissions import IsAuthenticatedAndIsStaff

from django_filters.rest_framework import DjangoFilterBackend

from boxes.models import Boxes


class ListAllBoxesView(generics.ListAPIView):
    """
    List all boxes present in the database.
    If user is not staff then remove creator and last updated field.
    """

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BoxUsernameDateFilter
    serializer_class = BoxSerializer
    queryset = Boxes.objects.all()

    def get_serializer_context(self):
        """
        Context is passed to check weather user is staff or not.
        """
        context = super(ListAllBoxesView, self).get_serializer_context()
        context.update({"user_is_staff": self.request.user.is_staff})
        return context


class BoxCreateView(generics.CreateAPIView):
    """
    API to create a new box and only the staff user can create a new box.
    """

    permission_classes = [IsAuthenticatedAndIsStaff]
    serializer_class = BoxSerializer

    def post(self, request):
        serializer = BoxSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=request.user)
        response = {
            "success": "True",
            "message": "Box created successfully",
        }
        return Response(response, status=status.HTTP_201_CREATED)


class BoxUpdateView(generics.UpdateAPIView):
    """
    API to update a box and only the staff user can update a box.
    Doesn't allow to update the creator and creation_date
    """

    permission_classes = [IsAuthenticatedAndIsStaff]
    serializer_class = BoxSerializer
    queryset = Boxes.objects.all()

    def patch(self, request, pk=None):
        box = Boxes.objects.get(pk=pk)
        serializer = BoxSerializer(
            box, data=request.data, context={"request": request}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            response = {
                "success": "True",
                "message": "Box updated successfully",
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                "success": "False",
                "message": "Operation unsuccessful",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ListMyBoxView(generics.ListAPIView):
    """
    API to list all the boxes created by the current staff user.
    """

    permission_classes = [IsAuthenticatedAndIsStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BoxFilter
    serializer_class = BoxSerializer

    def get_queryset(self):
        boxes_instance = Boxes.objects.filter(creator=self.request.user)
        return boxes_instance


class DestroyBoxView(generics.DestroyAPIView):
    """
    API to delete a box by uuid, and only be deleted
    if the loggedin user is the creator of the box.
    """

    permission_classes = [IsAuthenticatedAndIsStaff]

    def delete(self, request, pk=None):
        try:
            # Get the box instance by id and creator
            instance = Boxes.objects.get(id=pk, creator=request.user)
            instance.delete()
            response = {
                "success": "True",
                "message": "Box deleted successfully",
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "success": "False",
                "message": "Box cannot be deleted or unavailable",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
