from django.db import models


class Modem(models.Model):
    mac = models.CharField(max_length=17, unique=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mac


class Sensor(models.Model):
    mac = models.CharField(max_length=17, unique=True)
    modem = models.ForeignKey(Modem, on_delete=models.CASCADE, related_name='sensors')
    vibrations = models.IntegerField()
    temperature = models.IntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.mac


class Counter(models.Model):
    modem = models.ForeignKey(Modem, on_delete=models.CASCADE, related_name='counters')
    address = models.CharField(max_length=20)
    energy = models.FloatField()
    cos_fi_a = models.FloatField()
    cos_fi_b = models.FloatField()
    cos_fi_c = models.FloatField()
    cos_fi_common = models.FloatField()
    freq_a = models.FloatField()
    freq_b = models.FloatField()
    freq_c = models.FloatField()
    freq_common = models.FloatField()
    voltage_a = models.FloatField()
    voltage_b = models.FloatField()
    voltage_c = models.FloatField()
    voltage_common = models.FloatField()
    current_a = models.FloatField()
    current_b = models.FloatField()
    current_c = models.FloatField()
    current_common = models.FloatField()
    whole_power_a = models.IntegerField()
    whole_power_b = models.IntegerField()
    whole_power_c = models.IntegerField()
    active_power_a = models.IntegerField()
    active_power_b = models.IntegerField()
    active_power_c = models.IntegerField()
    reactive_power_a = models.IntegerField()
    reactive_power_b = models.IntegerField()
    reactive_power_c = models.IntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.address} - {self.timestamp}"
