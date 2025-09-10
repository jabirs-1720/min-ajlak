from rest_framework import serializers

from .models import Order

def generate_order_number():
    number = 1
    last_order = Order.objects.all().last()
    if last_order:
        number = last_order.number + 1
    return number

class OrderSerializer(serializers.ModelSerializer):
    # number = serializers.HiddenField(default=NumberDefault())
    number = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
    
    def create(self, validated_data):
        validated_data['number'] = generate_order_number()
        return super().create(validated_data)

