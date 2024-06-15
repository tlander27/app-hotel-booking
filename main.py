import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pd.read_csv("card_security.csv", dtype=str)
print(df)
print(f"type: {type(df)}")

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book a hotel by changing its availabilty to 'no'"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class Reservation:
    def __init__(self, cust_name, hotel_obj):
        self.cust_name = cust_name
        self.hotel = hotel_obj

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here is your reservation data:
        Name: {self.cust_name}
        Hotel: {self.hotel.name}
        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, exp_date, cvc, holder):
        card_data = {"number": self.number,
                     "expiration": exp_date,
                     "cvc": cvc,
                     "holder": holder}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False

if __name__ == "__main__":
    print(df)
    hotel_ID = input("Enter the hotel ID: ")
    hotel = Hotel(hotel_ID)

    if hotel.available():
        credit_card = SecureCreditCard(number="1234567890123456")
        if credit_card.validate(exp_date="12/26",
                                cvc="123",
                                holder="JOHN SMITH"):
            if credit_card.authenticate(given_password="mypass"):
                hotel.book()
                name = input("Enter your name: ")
                reservation = Reservation(cust_name=name, hotel_obj=hotel)
                print(reservation.generate())
            else:
                print("Credit card authentication failed.")
        else:
            print("There was a problem with your payment.")
    else:
        print("Hotel has no vacancy.")
