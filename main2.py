import pandas as pd
from abc import ABC, abstractmethod

df = pd.read_csv("hotels.csv", dtype={"id": str})


class Hotel:
    watermark = "The Real Estate Company"

    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    @classmethod
    def get_hotel_count(cls, data):
        return len(data)

    def __eq__(self, other):
        if self.hotel_id == other.hotel_id:
            return True
        else:
            return False

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

class Ticket(ABC):
    @abstractmethod
    def generate(self):
        pass

class Reservation(Ticket):
    def __init__(self, cust_name, hotel_obj):
        self.cust_name = cust_name
        self.hotel = hotel_obj

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here is your reservation data:
        Name: {self.the_customer_name}
        Hotel: {self.hotel.name}
        """
        return content

    @property
    def the_customer_name(self):
        name = self.cust_name.strip()
        name = name.title()
        return name

    # used as a utility function
    @staticmethod
    def convert(amount):
        return amount * 1.2

