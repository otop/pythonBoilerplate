import inspect
import trace
from collections import OrderedDict

import colorama

CACHE = OrderedDict()


def super_tracer(func):
    def inner(*args, **kwargs):
        tracer = trace.Trace(count=True, trace=False)
        result = tracer.runfunc(func, *args, **kwargs)
        metrics = tracer.results()

        func_data, start_func_line_no = inspect.getsourcelines(func)
        func_data = [i.rstrip() for i in func_data]

        global CACHE
        if not CACHE:
            CACHE = OrderedDict([(i, 0) for i in func_data])

        for k, v in metrics.counts.items():
            file_line_number = k[1]
            CACHE[func_data[file_line_number - start_func_line_no]] += v

        return result

    return inner


def statistics(dictionary):
    values = dictionary.values()
    max_val = max(values)
    d = OrderedDict([(k, v * 100.0 / max_val) for k, v in dictionary.items()])

    for k, v in d.items():
        prefix = colorama.Fore.BLUE
        if 80 < v <= 100:
            prefix = colorama.Fore.RED
        elif 60 < v <= 80:
            prefix = colorama.Fore.YELLOW
        elif 40 < v <= 60:
            prefix = colorama.Fore.GREEN
        elif 20 < v <= 40:
            prefix = colorama.Fore.CYAN
        print(prefix + k + "\t\t" + "{0:.0f}%".format(v))

    print(colorama.Style.RESET_ALL)


@super_tracer
def f(a):
    if a > 10:
        return "hell"
    return "hello"


if __name__ == "__main__":
    f(3)
    f(3)
    f(3)
    f(3)
    f(1)
    f(14)
    f(11)
    statistics(CACHE)
