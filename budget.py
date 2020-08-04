class Category:

    def __init__(self, name):
        self.ledger = []
        self.balance = 0.0
        self.name = name

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})
        self.balance += amount

    def withdraw(self, amount, description=''):
        if(not self.check_funds(amount)):
            return False
        self.ledger.append({'amount': amount*(-1), 'description': description})
        self.balance -= amount
        return True

    def get_balance(self):
        return self.balance

    def transfer(self, amount, bud_category):
        if(self.withdraw(amount, "Transfer to "+bud_category.name)):
            bud_category.deposit(amount, "Transfer from "+self.name)
            return True
        return False

    def check_funds(self, amount):
        if(self.balance < amount):
            return False
        return True

    def __str__(self):
        out_str = ""
        num_stars_beg = 0
        num_stars_end = 0
        if((30-len(self.name))%2 == 0):
            num_stars_beg = (30-len(self.name))/2
            num_stars_end = num_stars_beg
        else:
            num_start_beg = ((30-len(self.name))/2)-1
            num_stars_end = (30-len(self.name))/2
        stars_beg = "*"*int(num_stars_beg)
        stars_end = "*"*int(num_stars_end)
        out_str = stars_beg + self.name + stars_end + "\n"
        for transaction in self.ledger:
            if(len(transaction['description']) > 23):
                transaction['description'] = transaction['description'][0:23]
            num_spaces = 30 - (len(transaction['description']) + len("{:.2f}".format(transaction['amount'])))
            white_spaces = " " * num_spaces
            out_str += transaction['description'] + white_spaces + "{:.2f}".format(transaction['amount']) + "\n"
        out_str += "Total: "+"{:.2f}".format(self.balance)
        return out_str





def create_spend_chart(categories):
    total_withdrawal = 0
    category_withdrawal_list = []
    longest_string = ""
    for category in categories:
        if(len(category.name) > len(longest_string)):
            longest_string = category.name
        category_withdrawal = 0
        for transaction in category.ledger:
            if(transaction['amount'] < 0):
                category_withdrawal += (transaction['amount']*-1)
        category_withdrawal_list.append({"name": category.name, "total_withdrawal": category_withdrawal})
        total_withdrawal += category_withdrawal

    str_output = ""
    for x in reversed(range(0, 101, 10)):
        if(x == 100):
            string_line = str(x)+"| "
        elif( x == 0):
            string_line = "  "+str(x)+"| "
        else:
            string_line = " "+str(x)+"| "
        for category in category_withdrawal_list:
            percentage = 100 / total_withdrawal * category['total_withdrawal']
            if(percentage > x):
                string_line += "o"
            else:
                string_line += " "
            string_line += "  "
        string_line += "\n"
        str_output += string_line
    if(len(category_withdrawal_list) == 1):
        horizontal_line = "-"*4
    else:
        horizontal_line = "-"*(4+(3*(len(category_withdrawal_list)-1)))
    str_output += "    "+horizontal_line+"\n"
    for x in range(len(longest_string)):
        category_str = "     "
        for category in categories:
            if(x in range(len(category.name))):
                category_str += category.name[x] + "  "
            else:
                category_str += "   "
        str_output += category_str + "\n"

    return "Percentage spent by category\n"+str_output
