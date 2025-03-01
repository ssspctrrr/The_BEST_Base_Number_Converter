import decimal as dc

def get_base(prompt):
    while True:
        try:
            number = int(input(f"{prompt}\nPossible values: {list(range(2,37))}\n"))
            if number in range(2,37):
                return number
            else:
                raise Exception()
        except:
            print("Invalid value entered. Enter only valid value\n")
            
def get_number(from_base, number_range):
    while True:
        try:
            number = input("\nWhat is the number to be converted?\n").upper()

            if number == "": #raises error if input is an empty character
                raise Exception()
    
            for index in range(0, len(number)):
                if number[index] in [".","-"]:
                    point = number.count(".")
                    negative = number.count("-")
                    
                    if (point > 1) or (negative > 1): #raises error if there are more than 1 decimal point or negative symbol in the input
                        raise Exception()
                    elif number in (".", "-", "-.", ".-"): #raises error if the number is purely just those in the list
                        raise Exception()
                    elif ("-" in number) and ("-" != number[0]): #raises error if negative symbol is not in index 0
                        raise Exception()
                elif (number[index] not in number_range) or (number_range.find(number[index]) >= from_base): #raises error if there is a character that exceeds the base
                    raise Exception()
            else:
                return number
        except:
            print("Invalid value entered. There is a character that is not part of the base of your number.")
            continue
        
def get_fractional_places():
    while True:
        try:
            fractional_places = int(input("\nHow many fractional places should the result be if it needs rounding off?\n(Enter only 0 or positive integers)\n"))
            if fractional_places <= 0:
                raise Exception()
            else:
                return fractional_places
        except:
            print("Invalid value for fractional places. Try again.")
            continue
                   
def int_to_base10(number, number_range, from_base):
    result = 0
    
    if "-" in number: #remembers if the original number is negative
        number = number.replace("-", "")
        is_negative = True
    else:
        is_negative = False
    
    for index in range(0, len(number)):
        value = number_range.find(number[index])
        product = value * (from_base**(len(number) - 1 - index))
        result = product + result
    
    if is_negative == True:
        return str(result * -1)
    else:
        return str(result)

def int_from_base10(number, number_range, to_base):
    result = ""
    if "-" in number: #remembers if the original number is negative
        number = number.replace("-", "")
        is_negative = True
    else:
        is_negative = False
    number = int(number)
    
    while True:
        if number < to_base: #removes zero output if the number is less than the to_base
            result = number_range[number] + result
            break
        
        remainder = number % to_base #getting the values into the new base
        result = number_range[remainder] + result
        
        number = number // to_base #initiating the new value for number
    
    if is_negative == True:
        return "-" + result
    else:
        return result
    
def float_to_base10(number, number_range, from_base, fractional_places):
    result =  0
    for index in range(0, len(number)):
        multiplier = dc.Decimal((dc.Decimal(from_base ** ((index * -1)-1))))
        value = number_range.find(number[index])
        product = dc.Decimal(int(value)) * multiplier
        result = product + result

    if (len(str(result)) - 2) > fractional_places:
        result = round(result, fractional_places)
        return str(result)[1:]
    else:
        return str(result)[1:]
    
def float_from_base10(number, number_range, to_base, fractional_places):
    result = ""

    if dc.Decimal(number) == 0: #if user types in .0/.00/.000 or just 0, it will return the number itself 
        return number

    for product in range(0, fractional_places):
        if dc.Decimal(number) == 0: #if the number already reached 0 before hitting fractional_places, it will return the results already
            return ("." + result)
        
        product = dc.Decimal(number) * to_base
        str_product = str(product)
        point_index = str_product.find(".")
        value_index = int(str_product[0:point_index]) #gets the value that will become the converted character
        value = number_range[value_index] #uses the value and turns that into its equivalent character
        number = str_product[point_index:] #initialize the new number to be multiplied
        result = result + value #add the converted character
    else:
        return ("." + result)

while True: 
    from_base = get_base("\nThe number will be converted FROM BASE?")
    to_base = get_base("\nThe number will be converted TO BASE?")

    if from_base == to_base:
        print("\nBases entered are the same. The FROM BASE and TO BASE should be different.\n")
        continue
    else:
        break

def main():
    number_range = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    number = get_number(from_base, number_range)

    if "." in number:
        fractional_places = get_fractional_places()
        point_index = number.find(".")
        number_int = number[0:point_index]
        number_float = number[point_index:]
        
        if from_base == 10:
            int_final_result = int_from_base10(number_int, number_range, to_base)
            float_final_result = float_from_base10(number_float, number_range, to_base, fractional_places)
        elif to_base == 10:
            int_final_result = int_to_base10(number_int, number_range, from_base)
            float_final_result = float_to_base10(number_float[1:], number_range, from_base, fractional_places)
        else:
            int_initial_result = int_to_base10(number_int, number_range, from_base)
            int_final_result = int_from_base10(int_initial_result, number_range, to_base)

            float_initial_result = float_to_base10(number_float[1:], number_range, from_base, 9999)
            float_final_result = float_from_base10(float_initial_result, number_range, to_base, fractional_places)

        final_result = int_final_result + float_final_result
    else:
        if from_base == 10:
            final_result = int_from_base10(number, number_range, to_base)
        elif to_base == 10:
            final_result = int_to_base10(number, number_range, from_base)
        else:
            initial_result = int_to_base10(number, number_range, from_base)
            final_result = int_from_base10(initial_result, number_range, to_base)

    print(f"\n{number} in Base{from_base} is {final_result} in Base{to_base}.")

if __name__ == "__main__":
    main()