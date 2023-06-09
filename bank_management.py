
class Bank:
    def __init__(self) -> None:
        self.__user_list=[]
        self.__total_bank_balance=0
        self.__total_loan_amount=0
        self.__is_loan_available= True
    def get_bank_balance(self):
        return self.__total_bank_balance
    def show_total_loan_of_bank(self):
        return self.__total_loan_amount
    def make_loan_available(self):
        if self.__is_loan_available==True:
            print("Already loan available")
        else:
            self.__is_loan_available=True
            print("You have make the loan available")
    def make_loan_available_restricted(self):
        if self.__is_loan_available==False:
            print("Already loan is unavailable")
        else:
            self.__is_loan_available=False
            print("You have make the loan unavailable")
    
    def create_user(self,email,password):
        user=User(email,password)
        self.__user_list.append(user)
        return user
    def get_user_by_email(self, email):
        for user in self.__user_list:
            if user.get_email() == email:
                return user
        return False
    def is_valid_user(self,email,password):
        user=self.get_user_by_email(email)
        if user is not False:
            if user.password==password:
                return user
            else:
                return False
        else:
            return False

    def is_eligible_for_withdrawal(self,user,amount):
        if user.balance>=amount:
            return True
        else:
            return False
    def manage_withdrawal_in_user_wallet(self, user, amount):
        user.balance-=amount       
        user.transaction_history["total_withdrawal"]+=amount
        
            
    def is_eligible_for_loan(self,user,amount):
        if amount<=2*(user.balance):
            return True
        else:
            return False
    def manage_loan_in_user_wallet(self,user,amount):
        user.loan+=amount
        user.balance+=amount
        user.transaction_history["loan"]+=amount
    def manage_deposit_in_user_wallet(self,user,amount):
        user.balance+=amount
        user.transaction_history["total_deposited"]+=amount
       

    def deposit_amount(self,email,amount):
        user=self.get_user_by_email(email)
        if user is not False:
            self.manage_deposit_in_user_wallet(user,amount)
            self.__total_bank_balance+=amount
            print(f"{amount} taka is deposited successfully for {email}....")
        else:
            print(f"Failed!...There is no user registered on this email : {email}")
    def withdrawal_amount(self,email,password,amount):
        valid_user=self.is_valid_user(email,password)
        if valid_user is not False:
            if self.is_eligible_for_withdrawal(valid_user,amount)==True:
                if(self.__total_bank_balance>=amount):
                    self.manage_withdrawal_in_user_wallet(valid_user,amount)
                    self.__total_bank_balance-=amount
                    print(f"{amount} taka withdrawal is successful....")
                else:
                    print("The bank is bankrupt.....")
            else:
                print("Insufficient balance.....")
        else:
            print(f"Failed!...The email or pass is incorrect..")
    
    
    
    def give_loan (self,email,password,amount):
        if self.__total_bank_balance<amount:
            print('The bank is bankrupted')
            return False
        if self.__is_loan_available==True:
            user=self.is_valid_user(email,password)
            if user is not False:
                if self.is_eligible_for_loan(user,amount)== True:
                    self.manage_loan_in_user_wallet(user,amount)
                    self.__total_bank_balance-=amount
                    self.__total_loan_amount+=amount
                    print(f"Your loan of {amount} is granted...")
                else:
                    print("Not eligible for loan.. You want more than your capacity..")
            else:
                print("User is invalid or the credential is wrong....")
        else:
            print("Currently Bank is not giving any loan...")



    def balance_transfer(self,sender_email,sender_pass, receiver_email, amount):
        sender=self.is_valid_user(sender_email,sender_pass)
        receiver=self.get_user_by_email(receiver_email)
        if sender and receiver is not False:
            if self.__total_bank_balance<amount:
                print('The bank is bankrupted')
                return False
            if self.is_eligible_for_withdrawal(sender,amount)== True:
                self.manage_withdrawal_in_user_wallet(sender,amount)
                sender.transaction_history["send"]+=amount
                self.manage_deposit_in_user_wallet(receiver,amount)
                receiver.transaction_history["received"]+=amount
                print(f'{amount} taka is transferred to {receiver_email} from {sender_email} successfully...')
            else:
                print("The bank is bankrupt")
        else:
            print("Failed to transfer. Please give correct information")

        








class BaseUser:
    def __init__(self,email,password) -> None:
        self.email=email
        self.password=password
    def get_email(self):
        return self.email
    

class User(BaseUser):
    def __init__(self, email, password) -> None:
        super().__init__(email, password)
        self.balance=0
        self.transaction_history={"total_deposited":0,"total_withdrawal":0,"loan":0,"send":0,"received": 0}
        self.loan=0
    def show_my_balance(self):
        print(f'Balance of {self.email} is {self.balance}')
    def show_my_transaction_history(self):
        print(f'Transaction History for {self.email}\nTotal deposited so far is: {self.transaction_history["total_deposited"]} \nTotal withdrawal is : {self.transaction_history["total_withdrawal"]}\nTotal loan: {self.transaction_history["loan"]}\nBalance Send: {self.transaction_history["send"]} \nBalance Received: {self.transaction_history["received"]}')
class Admin(BaseUser):
    def __init__(self, email, password,bank) -> None:
        super().__init__(email, password) 
        self.__bank=bank
    def show_balance_of_bank(self):
        print(f"Total Balance in Bank: {self.__bank.get_bank_balance()}")
    def show_loan_of_bank(self):
        print(f"Total loan in Bank: {self.__bank.show_total_loan_of_bank()}")
    def make_loan_available(self):
        self.__bank.make_loan_available()
    def make_loan_unavailable(self):
        self.__bank.make_loan_available_restricted()
    
    


bank=Bank()
admin=Admin("admin@gm.com","admin",bank)

solayman=bank.create_user("mdso@gm.com","12234")
nuhin=bank.create_user("nuhin@n.com","nuha")

bank.deposit_amount("mdso@gm.com",5000000)
bank.deposit_amount("nuhin@n.com",15000)
bank.balance_transfer("nuhin@n.com","nuha","mdso@gm.com",1000)
nuhin.show_my_balance()
nuhin.show_my_transaction_history()
solayman.show_my_balance()
solayman.show_my_transaction_history()
bank.give_loan("nuhin@n.com","nuha",28000)
nuhin.show_my_balance()
nuhin.show_my_transaction_history()
solayman.show_my_transaction_history()
admin.show_balance_of_bank()
admin.show_loan_of_bank()