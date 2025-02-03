from rest_framework import serializers

from modems.models import *


class ModemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modem
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class CounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counter
        fields = '__all__'


class ModemDataSerializer(serializers.Serializer):
    mac = serializers.CharField()
    name1 = serializers.CharField()
    vibrations1 = serializers.ListField(child=serializers.FloatField())
    temperature1 = serializers.ListField(child=serializers.FloatField())
    name2 = serializers.CharField()
    vibrations2 = serializers.ListField(child=serializers.FloatField())
    temperature2 = serializers.ListField(child=serializers.FloatField())
    counters = serializers.ListField(child=serializers.DictField())
    time = serializers.ListField(child=serializers.CharField())
