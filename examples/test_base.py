from lantz.drivers.tektronix import TDS1012


from lantz_experiment.models import Device

dev = Device()
dev.driver = TDS1012.via_serial('1')
for feat in dev._features:
    print(feat)
