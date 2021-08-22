from rest_framework import serializers


class MsgSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    start = serializers.BooleanField(required=False)
    data = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance
