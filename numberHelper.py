'''
    Single point of truth for useful functions to handle 
    number conversions between ints and strings.

    numToWord() converts numbers to words.
'''

import math

def extendDigits(value:int, num_digits:int)->str:
    """ Creates a string that extends a number (with zeros in front)
        to have the required number of digits 

        Args:
            value (int): The number to extend
            num_digits (int): The amount to extend to

        Returns:
            str: The created string of format 00012 (if passed 12 & 5)
    """
    stringified_num = str(value)
    return '0'*(num_digits - len(stringified_num)) + stringified_num

def numToWord(num):
    '''
        Converts ints into strings
    '''
    numDict = {
        # there will never be a chapter zero, but this is needed
        # for numbers whos ones place of is zero (10, 20, 30, ...)
        '0': '', 
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'nine',
        '10': 'ten',
        '11': 'eleven',
        '12': 'twelve',
        '13': 'thirteen',
        '14': 'fourteen',
        '15': 'fifteen',
        '16': 'sixteen',
        '17': 'seventeen',
        '18': 'eighteen',
        '19': 'nineteen'
    }

    tensDigitDict = {
        '2': 'twenty',
        '3': 'thirty',
        '4': 'fourty',
        '5': 'fifty',
        '6': 'sixty',
        '7': 'seventy',
        '8': 'eighty',
        '9': 'ninety'
    }

    if num < 20:
        # since numbers 1-20 are weird have to hard code them
        toReturn = numDict[str(num)]
    
    elif num >= 20:
        # get the number that is contained in the tens and one digit
        tensDigit = math.trunc(num/10)
        onesDigit = num % 10 # mod by ten to get one's digit

        prefix =  tensDigitDict[str(tensDigit)]
        suffix = numDict[str(onesDigit)]

        if onesDigit != 0:
            toReturn = prefix + '-' + suffix
        else:
            toReturn = prefix

    return toReturn