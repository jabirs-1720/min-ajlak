from rest_framework import serializers

from authentication.defaults import DefaultRestaurant
from .models import Meal, OptionGroup, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'name', 'extra_price']

class OptionGroupSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = OptionGroup
        fields = ['id', 'name', 'allow_multiple', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        group = OptionGroup.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(group=group, **option_data)
        return group

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options')
        instance.name = validated_data.get('name', instance.name)
        instance.allow_multiple = validated_data.get('allow_multiple', instance.allow_multiple)
        instance.save()

        instance.options.all().delete()
        for option_data in options_data:
            Option.objects.create(group=instance, **option_data)
        return instance

class MealSerializer(serializers.ModelSerializer):
    restaurant = serializers.HiddenField(default=DefaultRestaurant())
    option_groups = OptionGroupSerializer(many=True, required=False)

    class Meta:
        model = Meal
        fields = ['id', 'restaurant', 'name', 'image', 'base_price', 'preparation_time', 'option_groups']

    def create(self, validated_data):
        groups_data = validated_data.pop('option_groups', [])
        meal = Meal.objects.create(**validated_data)
        for group_data in groups_data:
            options_data = group_data.pop('options')
            group = OptionGroup.objects.create(meal=meal, **group_data)
            for option_data in options_data:
                Option.objects.create(group=group, **option_data)
        return meal

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('option_groups', [])
        instance.name = validated_data.get('name', instance.name)
        instance.base_price = validated_data.get('base_price', instance.base_price)
        instance.preparation_time = validated_data.get('preparation_time', instance.preparation_time)
        instance.save()

        instance.option_groups.all().delete()
        for group_data in groups_data:
            options_data = group_data.pop('options')
            group = OptionGroup.objects.create(meal=instance, **group_data)
            for option_data in options_data:
                Option.objects.create(group=group, **option_data)
        return instance
