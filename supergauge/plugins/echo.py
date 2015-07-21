import sys


def write(text):
    if text.endswith("\n") is False:
        text += "\n"
    sys.stderr.write(text)
    sys.stderr.flush()


class Echo(object):
    def send(self, timestamp, metrics, dimensions):
        width = 50
        fill = "#"
        write(" dimensions ".center(width, fill))
        for key, val in dimensions.items():
            print("{0}: {1}".format(key, val))

        write(" timstamp ".center(width, fill))
        write(timestamp)

        write(" metrics ".center(width, fill))
        for name, val, unit in metrics:
            write("{0}={1} {2}".format(name, val, unit))
        return True
