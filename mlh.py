from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import csv

load_dotenv()

MLH_EMAIL = os.getenv("MLH_EMAIL")
MLH_PASSWORD = os.getenv("MLH_PASSWORD")

names = []
with open('names.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        first_name, last_name, id_number = row
        names.append((first_name, last_name, id_number))


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://organize.mlh.io/events/")
    page.get_by_text("Sign in now").click()
    page.get_by_placeholder("you@your-domain.com").fill(MLH_EMAIL)
    page.get_by_placeholder("Shhh! This is super secret.").fill(MLH_PASSWORD) 
    page.get_by_role("button", name="Sign In").click()
    
    #change this based on the event 
    page.get_by_role("link", name="End of Semester").click()
    page.get_by_role("link", name="Registrations").click()

    for name in names:
        page.get_by_role("link", name="Add attendee").click()
        page.get_by_placeholder("Enter their first name").fill(name[0])
        page.get_by_placeholder("Enter their last name").fill(name[1])
        page.get_by_placeholder("Enter their email address").fill(name[2] + "@nyu.edu")

        combobox = page.get_by_role("combobox", name="Registration Status")
        combobox.select_option(value="Checked In")
        page.get_by_role("button", name="Add Participant").click()
