import requests
from bs4 import BeautifulSoup
import time

# going to url
url_to_scrape = 'http://apps2.polkcountyiowa.gov/inmatesontheweb/'

# grabbing all there
r = requests.get(url_to_scrape)

# parsing it
soup = BeautifulSoup(r.text, "html.parser")

# placeholder
inmates_links = []

# looping though rows of inmates
for table_row in soup.select(".inmatesList tr"):
    # looking for all substrings with td key
    table_cells = table_row.findAll('td')
    # We need to find not only row but cells also
    # Lets check if there are at least one cell
    if len(table_cells) > 0:
        # taking part of direct links
        relative_link_to_inmate_details = table_cells[0].find('a')['href']
        # making absolute link
        absolute_link_to_inmate_details = url_to_scrape + relative_link_to_inmate_details
        # adding absolute links to list
        inmates_links.append(absolute_link_to_inmate_details)

# placeholder for inmates
inmates = []

# Loop over inmates direct link
for inmates_link in inmates_links[:2]:

    # getting HTML from direct link
    r = requests.get(inmates_link)
    soup = BeautifulSoup(r.text, "html.parser")

    # Putting what we need in dictionary
    inmate_details = {}

    # Getting all of table rows in inmateProfile table
    inmate_profile_rows = soup.select("#inmateProfile tr")
    # Inmate age
    #  From looking at the HTML source (using View Source in our browser)
    #  we see that age is in the first row and the first table cell (td)
    #  We use the strip function to cleanup unwanted spaces
    inmate_details['age'] = inmate_profile_rows[0].findAll('td')[0].text.strip()
    # Same with race
    inmate_details['race'] = inmate_profile_rows[3].findAll('td')[0].text.strip()
    # Sex
    inmate_details['sex'] = inmate_profile_rows[4].findAll('td')[0].text.strip()

    # Getting all of table rows in inmateNameDate table
    inmate_name_date_rows = soup.select("#inmateNameDate tr")
    # Name
    inmate_details['name'] = inmate_name_date_rows[1].findAll('td')[0].text.strip()
    # Date
    inmate_details['booked_at'] = inmate_name_date_rows[2].findAll('td')[0].text.strip()

    # Getting all of table rows in inmateNameDate table
    inmate_address_container = soup.select("#inmateAddress")
    inmate_details['city'] = inmate_address_container[0].text.split('\n')[2].strip()

    # All done, adding our dictionary list
    inmates.append(inmate_details)

    # We need to make a pause to don't overwhelm website
    # time.sleep(1)

# Now we have details for each in dictionary
# Lets print it
for inmate in inmates:
    print('{0}, {1}'.format(inmate['name'], inmate['age']))
    print('{0} {1} from {2}'.format(inmate['race'], inmate['sex'], inmate['city']))
    print('Booked at {0}'.format(inmate['booked_at']))
    print()