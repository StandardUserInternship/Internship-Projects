# Read through the following script, identify issues, and fix the bug(s):

    """
    Finds and returns the largest number in a list
    """
    def find_largest(list_of_numbers):
       first_number = None
       for number in list_of_numbers:
           try:
               if first_number is None or number > first_number:
                   first_number = number
                   break
           except Exception as e:
               print(e.with_traceback)
               continue
       return first_number

    """
    Gets and validates 5 numbers from the user
    Returns the five numbers as a list
    """
    def get_user_input():
       while True:
           user_numbers = []
           try:
               for i in range(1,6):
                   user_number = input(f"Enter a whole number {i}/5): ")
                   user_numbers.append(int(user_number))
               return user_numbers
           except ValueError:
               print("The last number you entered is an invalid number.\n")
               continue


    """
    Main Function
    Ignore for the purposes of this assignment
    """
    if __name__ == "__main__":
       numbers = get_user_input()
       print(f"The largest number that you entered is {find_largest(numbers)}")
