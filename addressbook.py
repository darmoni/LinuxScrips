#!/usr/bin/env python3

# $Id$ $Date$

#from addressbook3_pb2 import AddressBook, RqstAgentStatus, RqstReadAddressBook, Person
from addressbook_pb2 import AddressBook, RqstAgentStatus, RqstReadAddressBook, Person
import sys, os
def ask_agent_status(id):
    status_request=RqstAgentStatus()
    status_request.id=id
    f = open('agent_id_request', "wb")
    f.write(status_request.SerializeToString())
    f.close()
    exit(0)

def GetAgentStatus(agent_id):
    q="SELECT call_status FROM agent_data WHERE account_id = {};".format(agent_id)
    return (q)

def ReadCommandFromFile(command_filename = 'commands', answer_filename = 'response'):
    try:
        f = open(command_filename, "rb")
        request = RqstReadAddressBook()
        request.ParseFromString(f.read())
        f.close()
        print("{}".format(request))
        # Read the existing address book.

        address_book = AddressBook()

        try:
            f = open(request.filename, "rb")
            address_book.ParseFromString(f.read())
            f.close()
        except IOError:
            print (sys.argv[1] + ": Could not open file.  Creating a new one.")

        f = open(answer_filename, "wb")
        f.write(address_book.SerializeToString())
        f.close()
        #ListPeople(address_book)

    except IOError:
        print (sys.argv[1] + ": Could not open file.  Creating a new one.")
    exit(0)

# This function fills in a Person message based on user input.
def PromptForAddress(person):
    print ("Enter person ID number: ")
    test_id = sys.stdin.readline().strip()
    if '' == test_id:
        del person
        return -1
    person.id = int(test_id)
    if person.id > 0:
        print ("Enter name: ")
        person.name = sys.stdin.readline().strip()#raw_input("Enter name: ")

        print ("Enter email address (blank for none): ")
        email = sys.stdin.readline().strip()#raw_input("Enter email address (blank for none): ")
        if email != "":
            person.email = email

        while True:
            print ("Enter a phone number (or leave blank to finish): ")
            number = sys.stdin.readline().strip()#raw_input("Enter a phone number (or leave blank to finish): ")
            if number == "":
                break

            phone_number = person.phones.add()
            phone_number.number = number
            print ("Is this a mobile, home, or work phone? ")
            type = sys.stdin.readline().strip()#raw_input("Is this a mobile, home, or work phone? ")
            if type == "mobile":
                phone_number.type = Person.MOBILE
            elif type == "home":
                phone_number.type = Person.HOME
            elif type == "work":
                phone_number.type = Person.WORK
            else:
                print ("Unknown phone type; leaving as default value.")
    return person.id

# Iterates though all people in the AddressBook and prints info about them.
def ListPeople(address_book):
    for person in address_book.people:
        print ("Person ID:", person.id)
        print ("  Name:", person.name)
        if person.HasField('email'):
            print ("  E-mail address:", person.email)

        for phone_number in person.phones:
            if phone_number.type == Person.MOBILE:
                print ("  Mobile phone #: "),
            elif phone_number.type == Person.HOME:
                print ("  Home phone #: "),
            elif phone_number.type == Person.WORK:
                print ("  Work phone #: "),
            print (phone_number.number)

# Main procedure:  Reads the entire address book from a file,
#   adds one person based on user input, then writes it back out to the same
#   file.
agent_id_request_fname='agent_id_request'
if os.path.isfile(agent_id_request_fname):
    status_request=RqstAgentStatus()
    f = open(agent_id_request_fname, "rb")
    status_request.ParseFromString(f.read())
    f.close()
    print(GetAgentStatus(status_request.id))

if len(sys.argv) != 2:
    print ("Usage:", sys.argv[0], "ADDRESS_BOOK_FILE")

person = Person()
person.id = 1234
person.name = "John Doe"
person.email = "jdoe@example.com"
phone = person.phones.add()
phone.number = "555-4321"
phone.type = Person.HOME
try:
    person.no_such_field = 1  # raises AttributeError
except Exception as E:
    print (str(E))
try:
    person.id = "1234"        # raises TypeError
except Exception as E:
    print (str(E))

if person.IsInitialized():
    print (person)

# Read the existing address book.

address_book = AddressBook()

try:
    f = open(sys.argv[1], "rb")
    address_book.ParseFromString(f.read())
    f.close()
except IOError:
    print (sys.argv[1] + ": Could not open file.  Creating a new one.")

ListPeople(address_book)

# Add an address.
PromptForAddress(address_book.people.add())

ListPeople(address_book)
print ("Save this Data?")
save = sys.stdin.readline().strip().lower()
if 'yes' == save:
    # Write the new address book back to disk.
    f = open(sys.argv[1], "wb")
    f.write(address_book.SerializeToString())
    f.close()
