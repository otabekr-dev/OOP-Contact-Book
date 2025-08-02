import json
from rich.console import Console
from rich.table import Table
from contact_book.models.contact import Contact
from contact_book.services.db import DB


class ContactBook:

    def __init__(self):
        self.console = Console()
        self.db = DB()

    def print_menu(self):
        self.console.print('[bold italic yellow on red blink]\n======== Menu ========')
        self.console.print(
            '1. Add New Contact\n'
            '2. Show All Contacts\n'
            '3. Search Contact\n'
            '4. Update Contact\n'
            '5. Delete Contact\n'
            '6. Exit\n'
        )

    def add_contact(self):
        self.console.print("[bold green]Enter A New Contact Information")
        name = input("Name: ").strip().title()
        phone = input("Phone: ").strip()
        email = input("Email: ").strip()

        self.db.add_contact(name, phone, email)

    def print_contacts(self):
        table = Table(title="[bold blue]Contacts Table")

        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Phone", justify="right", style="green")
        table.add_column("Email", style="blue")

        for contact in self.db.get_contacts():
            table.add_row(
                contact.contact_id,
                contact.name,
                contact.phone,
                contact.email
            )

        self.console.print(table)

    def remove_contact(self):
        name_2_del = input('Ismni kiriting: ').strip().title()
        all_c = self.db.get_contacts()
        new_contacts = []

        for contact in all_c:
            if contact.name != name_2_del:
                new_contacts.append(contact)

        
        if len(new_contacts) < len(all_c):
            self.db.contacts = new_contacts
            self.db.save_contacts()
            self.console.print("[green]Contact successfully deleted!")
        else:
            self.console.print("[red]Contact not found.")




    def update_contact(self):
        uc = input('Yangilamoqchi bulgan kontaktingizni ismini kiriting: ').strip().title()

        all_contacts = self.db.get_contacts()
        updated = False

        for contact in all_contacts:
            if contact.name == uc:
                print('Yangi malumotlarni kiriting: ')
                u_name = input('Ism: ')
                u_phone = input('Telefon raqam: ')
                u_email = input('email: ')

                if u_name:
                    contact.name = u_name
                if u_phone:
                    contact.phone = u_phone
                if u_email:
                    contact.email = u_email

                updated = True
                break
        if updated :
            self.db.contacts = all_contacts
            self.db.save_contacts()
            self.console.print('[green] Kontakt malumotlari yangilandi')
        else:
            self.console.print('[red] Mavjud bulmagan kontakt')                        

    def search_contact(self):
        search = input("Search: ").strip().lower()
        
        table = Table(title="[bold blue]Found Contacts Table")

        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Phone", justify="right", style="green")
        table.add_column("Email", style="blue")

        for contact in self.db.get_contacts():
            if search in contact.name.lower() or search in contact.email.lower() or search in contact.phone:
                table.add_row(
                    contact.contact_id,
                    contact.name,
                    contact.phone,
                    contact.email
                )

        self.console.print(table)

    def run(self):
        print("salom, Contact Book Projectga Xush Kelibsiz!")
        while True:
            self.print_menu()

            choice = input("> ")
            if choice == '1':
                self.add_contact()
            elif choice == '2':
                self.print_contacts()
            elif choice == '3':
                self.search_contact()
            elif choice == '4':
                self.update_contact()
            elif choice == '5':
                self.remove_contact()
            elif choice == '6':
                break
            else:
                print("Mavjud bo'lmagan buyruq")                
