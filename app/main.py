import inspect
import trace
from collections import OrderedDict

import colorama

# {"func_first_line" : {"line": count}, ...}
LOOKUP_CACHE = dict()


def super_tracer(func):
    def inner(*args, **kwargs):
        global LOOKUP_CACHE

        tracer = trace.Trace(count=True, trace=False)
        result = tracer.runfunc(func, *args, **kwargs)
        metrics = tracer.results()

        func_data, start_func_line_no = inspect.getsourcelines(func)
        func_data = [i.rstrip() for i in func_data]

        func_first_line = func_data[1]  # because 0 is super_trace decorator
        data = LOOKUP_CACHE.get(func_first_line)
        if not data:
            LOOKUP_CACHE[func_first_line] = OrderedDict([(i, 0) for i in func_data])

        for key, value in metrics.counts.items():
            file_line_number = key[1]       # since metrics.counts' key will be (file_name, count)
            LOOKUP_CACHE[func_first_line][func_data[file_line_number - start_func_line_no]] += value

        return result

    return inner


def statistics(dictionary):
    values = dictionary.values()
    max_val = values[2]     # this is the first line of function
    d = OrderedDict([(k, v * 100.0 / max_val) for k, v in dictionary.items()])

    for k, v in d.items():
        prefix = colorama.Fore.BLUE
        if v > 100:
            prefix = colorama.Fore.MAGENTA
        elif 80 < v <= 100:
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


@super_tracer
def super_duper_func(a, b, c):
    if a < b:
        return 1
    if b > c:
        return 2
    if c < a:
        for el in range(100):
            a += 1
        return a + b
    return b + a + c


if __name__ == "__main__":
    super_duper_func(1, 2, 3)
    super_duper_func(4, 8, 21)
    super_duper_func(7, 1, 34)
    super_duper_func(8, 45, 0)
    super_duper_func(2, 8, 1)
    super_duper_func(90, 4, 7)
    f(3)
    f(3)
    f(3)
    f(3)
    f(1)
    f(14)
    f(11)
    f(14)
    f(14)
    f(14)
    f(14)
    f(14)
    for func_name, dt in LOOKUP_CACHE.items():
        pluses = "+++++++++++++"
        print pluses + func_name + pluses
        statistics(dt)
