from django.db import models


class Modem(models.Model):
    mac = models.CharField(max_length=17, unique=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mac


class Sensor(models.Model):
    mac = models.CharField(max_length=17, unique=True)
    modem = models.ForeignKey(Modem, on_delete=models.CASCADE, related_name='sensors')
    vibrations = models.JSONField()
    temperature = models.JSONField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.mac


class Counter(models.Model):
    modem = models.ForeignKey(Modem, on_delete=models.CASCADE, related_name='counters')
    address = models.CharField(max_length=20)
    energy = models.JSONField()
    cos_fi_a = models.JSONField()
    cos_fi_b = models.JSONField()
    cos_fi_c = models.JSONField()
    cos_fi_common = models.JSONField()
    freq_a = models.JSONField()
    freq_b = models.JSONField()
    freq_c = models.JSONField()
    freq_common = models.JSONField()
    voltage_a = models.JSONField()
    voltage_b = models.JSONField()
    voltage_c = models.JSONField()
    voltage_common = models.JSONField()
    current_a = models.JSONField()
    current_b = models.JSONField()
    current_c = models.JSONField()
    current_common = models.JSONField()
    whole_power_a = models.JSONField()
    whole_power_b = models.JSONField()
    whole_power_c = models.JSONField()
    active_power_a = models.JSONField()
    active_power_b = models.JSONField()
    active_power_c = models.JSONField()
    reactive_power_a = models.JSONField()
    reactive_power_b = models.JSONField()
    reactive_power_c = models.JSONField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.address} - {self.timestamp}"