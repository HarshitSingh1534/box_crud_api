import datetime
from rest_framework import serializers
from django.db.models import Avg
from boxes.models import Boxes
from django.conf import settings


class BoxSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")
    last_updated = serializers.ReadOnlyField()

    class Meta:
        model = Boxes
        fields = (
            "id",
            "height",
            "length",
            "breadth",
            "area",
            "volume",
            "creator",
            "last_updated",
        )
        read_only_fields = (
            "area",
            "volume",
            "creator",
            "last_updated",
        )
        extra_kwargs = {
            "height": {"required": True},
            "length": {"required": True},
            "breadth": {"required": True},
        }

    def create(self, attr):
        if attr["height"] <= 0:
            raise serializers.ValidationError(
                {"height": "Height must be greater than 0."}
            )
        if attr["length"] <= 0:
            raise serializers.ValidationError(
                {"length": "Length must be greater than 0."}
            )
        if attr["breadth"] <= 0:
            raise serializers.ValidationError(
                {"breadth": "Breadth must be greater than 0."}
            )

        # Condition 1:
        avg_area = Boxes.objects.all().aggregate(Avg("area"))

        # if there are no boxes in the database, then avg_area will be None
        avg_area["area__avg"] = (
            0 if avg_area["area__avg"] is None else avg_area["area__avg"]
        )

        # calculate the area of the box that we are going to add
        current_area = 2 * (
            attr["height"] * attr["length"]
            + attr["height"] * attr["breadth"]
            + attr["length"] * attr["breadth"]
        )

        # find the average of all the boxes in database including the current box that we are adding
        # so that we can check wether the current box that we are adding is voilating the average area condition
        avg_area["area__avg"] = (avg_area["area__avg"] + current_area) / 2

        if avg_area["area__avg"] > settings.A1:
            raise serializers.ValidationError(
                {
                    "area_error": "The dimension provided exceeds the average area limit, try with smaller dimensions."
                }
            )

        past_week = datetime.date.today() - datetime.timedelta(days=7)

        # Condition 3:
        total_boxes_in_last_week = Boxes.objects.filter(
            date_created__range=(past_week, datetime.datetime.now())
        ).count()
        if total_boxes_in_last_week >= settings.L1:
            raise serializers.ValidationError(
                {"error": "The total boxes created in the past week exceed the limit."}
            )

        # to get the authenticated user type
        request = self.context.get("request", None)
        if request:
            # Condition 2:
            avg_volume = Boxes.objects.filter(creator=request.user).aggregate(
                Avg("volume")
            )
            # if there are no boxes in the database, then avg_volume will be None
            avg_volume["volume__avg"] = (
                0 if avg_volume["volume__avg"] is None else avg_volume["volume__avg"]
            )

            # calculate the area of the box that we are going to add
            current_volume = attr["height"] * attr["length"] * attr["breadth"]

            # find the average of all the boxes in database including the current box that we are adding
            # so that we can check wether the current box that we are adding is voilating the average volume condition
            avg_volume["volume__avg"] = (avg_volume["volume__avg"] + current_volume) / 2

            if avg_volume["volume__avg"] > settings.V1:
                raise serializers.ValidationError(
                    {
                        "volume_error": "The dimension provided exceeds the average volume limit, try with smaller dimensions."
                    }
                )

            # Condition 4:
            total_boxes_created_by_user_in_last_week = Boxes.objects.filter(
                creator=request.user,
                date_created__range=(past_week, datetime.datetime.now()),
            ).count()

            if total_boxes_created_by_user_in_last_week >= settings.L2:
                raise serializers.ValidationError(
                    {
                        "error": "The total boxes created by you in the past week exceeds the limit."
                    }
                )
        return super(BoxSerializer, self).create(attr)

    def update(self, instance, validated_data):
        # if validated data is empty
        if len(validated_data) == 0:
            raise serializers.ValidationError(
                {
                    "invalid data": "Invalid data provided. Try with height, length and breadth."
                }
            )

        # if patch request is made and there is no height in the request body
        # so to avoid server error we are using instance.height instead of validated_data.get("height")
        # same goes for length and breadth as well
        if validated_data.get("height", instance.height) <= 0:
            raise serializers.ValidationError(
                {"height": "Height must be greater than 0."}
            )
        if validated_data.get("length", instance.length) <= 0:
            raise serializers.ValidationError(
                {"length": "Length must be greater than 0."}
            )
        if validated_data.get("breadth", instance.breadth) <= 0:
            raise serializers.ValidationError(
                {"breadth": "Breadth must be greater than 0."}
            )

        # Assuming :
        # 1. Average area of all added boxes should not exceed A1
        # 2. Average volume of all boxes added by the current user shall not exceed V1
        # should be check at the time of ceation of the box as the statments mentions the added keywork not update.
        return super(BoxSerializer, self).update(instance, validated_data)

    def __init__(self, *args, **kwargs):

        # if user is not staff then remove last_updated and creator field from the serializer
        context = kwargs.get("context", None)
        user_is_staff = context.get("user_is_staff", None)
        if user_is_staff is not None:
            if not user_is_staff:
                remove_fields = ["last_updated", "creator"]
                for field_name in remove_fields:
                    self.fields.pop(field_name)

        super(BoxSerializer, self).__init__(*args, **kwargs)
