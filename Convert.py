import conversion_rounding as cr  # make sure this file exists with to_AUD and to_USD functions

def convert(question):
    convert_to_usd = 1

    while True:
        try:
            to_convert = float(input(question))
            break
        except ValueError:
            print("Please enter a valid number (digits only).")

    if convert_to_usd:
        answer = cr.to_USD(to_convert)
        answer_statement = f"{to_convert} NZD is {answer} USD"
    else:
        answer = cr.to_AUD(to_convert)
        answer_statement = f"{to_convert} NZD is {answer} AUD"

    return answer_statement

# Main program
answer2 = convert("Enter a number to convert: ")
print(f"Conversion result: {answer2}")
