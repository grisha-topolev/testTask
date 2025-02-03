from datetime import datetime
from typing import List, Dict, Any

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.request import Request

from modems.models import Modem, Sensor, Counter
from modems.api.v1.serializers import ModemSerializer, SensorSerializer, CounterSerializer, ModemDataSerializer


class ModemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Modem.objects.all()
    serializer_class = ModemSerializer


class SensorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class CounterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Counter.objects.all()
    serializer_class = CounterSerializer


class EntityProcessor:
    def __init__(self, data: Dict[str, Any], timestamp: datetime):
        self.data = data
        self.timestamp = timestamp

    def process(self) -> None:
        raise NotImplementedError


class ModemProcessor(EntityProcessor):
    def process(self) -> Modem:
        modem, _ = Modem.objects.get_or_create(mac=self.data['mac'])
        return modem


class SensorProcessor(EntityProcessor):
    def __init__(self, modem: Modem, data: Dict[str, Any], timestamp: datetime):
        super().__init__(data, timestamp)
        self.modem = modem

    def process(self) -> None:
        self._create_or_update_sensor(
            mac=self.data['name1'],
            vibrations=self.data['vibrations1'],
            temperature=self.data['temperature1']
        )
        
        self._create_or_update_sensor(
            mac=self.data['name2'],
            vibrations=self.data['vibrations2'],
            temperature=self.data['temperature2']
        )

    def _create_or_update_sensor(self, mac: str, vibrations: float, temperature: float) -> None:
        Sensor.objects.update_or_create(
            mac=mac,
            defaults={
                'modem': self.modem,
                'vibrations': vibrations,
                'temperature': temperature,
                'timestamp': self.timestamp,
            }
        )


class CounterProcessor(EntityProcessor):
    def __init__(self, modem: Modem, data: List[Dict[str, Any]], timestamp: datetime):
        super().__init__(data, timestamp)
        self.modem = modem

    def process(self) -> None:
        for counter_data in self.data:
            self._create_counter(counter_data)

    def _create_counter(self, counter_data: Dict[str, Any]) -> None:
        Counter.objects.create(
            modem=self.modem,
            timestamp=self.timestamp,
            **counter_data
        )


@api_view(['POST'])
def process_modem_data(request: Request) -> Response:
    serializer = ModemDataSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            data = serializer.validated_data
            timestamps = parse_timestamps(data['time'])
            
            modem_processor = ModemProcessor(data, timestamps[0])
            modem = modem_processor.process()
            
            sensor_processor = SensorProcessor(modem, data, timestamps[0])
            sensor_processor.process()
            
            counter_processor = CounterProcessor(modem, data['counters'], timestamps[0])
            counter_processor.process()

        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def parse_timestamps(time_strings: List[str]) -> List[datetime]:
    return [
        datetime.strptime(t, "%Y/%m/%d %H:%M:%S") for t in time_strings
    ]
