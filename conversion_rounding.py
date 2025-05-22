def round_ans(val):
    """
    Rounds value to the nearest whole number
    :param val: Number to be rounded
    :return: Rounded number as a string
    """
    var_rounded = (val * 2 + 1) // 2
    return "{:.0f}".format(var_rounded)


def to_AUD(nzd):
    """
    Converts from NZD to AUD
    :param nzd: Amount in NZD
    :return: Converted amount in AUD (2 decimal places)
    """
    exchange_rate = 0.9191
    converted = nzd * exchange_rate
    return f"{converted:.2f}"


def to_USD(nzd):
    """
    Converts from NZD to USD
    :param nzd: Amount in NZD
    :return: Converted amount in USD (2 decimal places)
    """
    exchange_rate = 0.5903
    converted = nzd * exchange_rate
    return f"{converted:.2f}"


def to_GBP(nzd):
    """
    Converts from NZD to GBP
    :param nzd: Amount in NZD
    :return: Converted amount in GBP (2 decimal places)
    """
    exchange_rate = 0.4402  # Example rate, adjust as needed
    converted = nzd * exchange_rate
    return f"{converted:.2f}"

# Main routine / Testing starts here
# to_c_test = [0, 100, -459]
# to_f_test = [0, 100, 40, -273]
#
# for item in to_f_test:
#     ans = to_fahrenheit(item)
#     print(f"{item} C is {ans} F")
#
# print()
#
# for item in to_c_test:
#     ans = to_celsius(item)
#     print(f"{item} F is {ans} C")
#
