class Echo(object):
    def send(self, timestamp, metrics, dimensions):
        width = 50
        fill = "#"
        print(" dimensions ".center(width, fill))
        for key, val in dimensions.items():
            print("{0}: {1}".format(key, val))

        print(" timstamp ".center(width, fill))
        print(timestamp)

        print(" metrics ".center(width, fill))
        for name, val, unit in metrics:
            print("{0}={1} {2}".format(name, val, unit))
        return True
