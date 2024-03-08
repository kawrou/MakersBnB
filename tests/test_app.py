from lib.user_repository import UserRepository
from lib.user import User
from playwright.sync_api import Page, expect

# Tests for your routes go here

"""
We can render the index page
"""
# def test_get_index(page, test_web_address):
#     # We load a virtual browser and navigate to the /index page
#     page.goto(f"http://{test_web_address}/index")

#     # We look at the <p> tag
#     strong_tag = page.locator("p")

#     # We assert that it has the text "This is the homepage."
#     expect(strong_tag).to_have_text("This is the homepage.")



# LOGIN.HTML TESTS

"""
When we GET the login page, 
it renders the template and its elements correctly
"""
def test_get_login(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")
    
    # A little messy as I was having difficulty testing the page's <title> element. Left some comments as useful for learning & documentation purposes. 
    title_tag = page.locator("title")
    print(title_tag)
    actual_title = title_tag.text_content() # <-- A way to get text content of a DOM element
    print(f"URL: {page.url}")
    print(f"Actual title: {actual_title}")
    print(f"Type of title: {type(actual_title)}")
    title_text = page.title() # <-- Alternative way to get visiblity on Title of page
    print(f"Actual title: {title_text}")
    print(f"Type of title: {type(title_text)}")
    #page.screenshot(path='screenshot.png') <-- A way to capture a screenshot of the page at the point in time
    expected_title = "MakersBnB"
    print(f"Type of expected title: {type(expected_title)}")
    # expect(title_tag).to_have_text("MakersBnB") <-- This "expect" isn't working. Using the pytest assert below instead. Maybe because it's in <head>?
    assert actual_title == "MakersBnB"
    
    
    nav_text = page.locator(".navbar-brand")
    h2_tag = page.locator("h2")
    create_account_link_text = page.locator(".forms_container .forward-button")
    footer_tag = page.locator("footer")

    expect(nav_text).to_have_text("MakersBnB")
    expect(h2_tag).to_have_text("Sign In")
    expect(create_account_link_text).to_have_text("Don't have an account? Click here to sign up!")
    expect(footer_tag).to_have_text("©MakerBnB")

"""
When a user logs in to the website, 
It should validate the user login details
If user credentials are wrong or do not exist
An error message should flash on the page
"""

def test_login_fail(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill('#username_input input', 'testuser') #<-- Incorrect user. Not in test databse
    page.fill('input[name=password]', 'Testpassword1@') #<-- incorrect password. Not in test database

    page.click('input[name=submit]')
    assert page.url == f"http://{test_web_address}/login"
    flash_message = page.inner_text('.flashes li')
    assert flash_message == "Invalid username or password. Please try again."
    

"""
When a user logs in to the website, 
It should validate the user login details
If user credentials are correct & exists
User should be redirected to their profile page
"""

def test_login_success(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb.sql")

    page.goto(f"http://{test_web_address}/login")
    page.fill('#username_input input', 'test') 
    page.fill('#password_input input', '123abcD!') #<-- Stored as hash in test database
    page.click('.button')
    
    assert page.url == f"http://{test_web_address}/profile"

    #This can all be placed and/or come from a test for /profile
    nav_text = page.locator(".navbar-brand")
    create_listing_link = page.locator(".container .btn")
    profile_listings_title_tag = page.locator(".container #profile_listings_h3")
    profile_listings_list = page.locator("#listed-spaces-list")

    # listings_text = profile_listings_list.text_content().strip()
    # listings_text_2 = profile_listings_list.inner_text()
    # print(f"text_content: {listings_text}")
    # print(f"inner_text: {listings_text_2}")
    
    # assert listings_text == ""

    # image_selector = 'img[data-src="static//images/(image_file_name)]'

    my_bookings_title_tag = page.locator(".container #profile_bookings_h3")
    profile_booked_spaces_list = page.locator("#booked-spaces-list")
    footer_tag = page.locator("footer")

    expect(nav_text).to_have_text("MakersBnB")
    expect(create_listing_link).to_have_text("Create New Listing")
    expect(profile_listings_title_tag).to_have_text("My Listings")
    expect(profile_listings_list).to_have_text("")
    expect(my_bookings_title_tag).to_have_text("My Bookings")
    expect(profile_booked_spaces_list).to_have_text("")
    expect(footer_tag).to_have_text("©MakerBnB")



#INDEX.HTML TESTS

"""
When we call index.html, it renders the template
"""

def test_get_index(page, test_web_address):
    page.goto(f"http://{test_web_address}")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Welcome to MakersBnB")

"""
When we got to the index page, it shows all listings on the page
"""
def test_get_index_listings(page, test_web_address, db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    page.goto(f"http://{test_web_address}")
    list_items = page.locator(".image-container")
    expect(list_items).to_have_text(['\n\n\n'            
                                    'Opulent Oak Haven£300 per night\n\n\n'            
                                    'Stonegate Sanctuary£560 per night\n\n\n'
                                    'Glass Vista Retreat£720 per night\n\n\n'            
                                    'Remote Hillside Lodge£110 per night\n\n\n'            
                                    'Alpine Oasis£150 per night\n\n\n'            
                                    'Stone Serenity£340 per night\n\n\n'            
                                    'Garden View Haven£80 per night\n\n'] )
    
"""
When we click on sign in page, it redirects us to the correct page
"""
def test_get_sign_in_page_from_landing_page(page, test_web_address):
    page.goto(f"http://{test_web_address}")
    page.click(".navbar-nav :nth-child(1) .nav-link")
    assert page.url == f"http://{test_web_address}/login"


"""
When click on create account, it shows us the create account page
"""
def test_get_creat_account_page_from_landing_page(page, test_web_address):
    page.goto(f"http://{test_web_address}")
    page.click(".navbar-nav :nth-child(2) .nav-link")
    assert page.url == f"http://{test_web_address}/create_account"


"""
When user is signed in, it displays you are logged in
"""
def test_nav_bar_displays_user_logged_in_on_index(page, test_web_address, db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    page.goto(f"http://{test_web_address}/login")
    page.fill("#username_input input", "test")#<-- Stored in test database
    page.fill("#password_input input", "123abcD!")#<-- Stored as hash in test database
    page.click(".button")
    page.click(".navbar-nav :nth-child(2) .nav-link")
    user_tag = page.locator(".navbar-nav :nth-child(1) .nav-link")
    sign_out_tag = page.locator(".navbar-nav :nth-child(2) .nav-link")
    assert page.url == f"http://{test_web_address}/"
    expect(user_tag).to_have_text("Hi, test")
    expect(sign_out_tag).to_have_text("Sign Out")

"""
When the user has signed out, it shows the the sign in and create account buttons
"""
def test_nav_bar_displays_user_logged_out_on_index(page, test_web_address, db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    page.goto(f"http://{test_web_address}/login")
    page.fill("#username_input input", "test")#<-- Stored in test database
    page.fill("#password_input input", "123abcD!")#<-- Stored as hash in test database
    page.click(".button")
    page.click(".navbar-nav :nth-child(2) .nav-link")
    assert page.url == f"http://{test_web_address}/"
    page.click(".navbar-nav :nth-child(2) .nav-link")
    assert page.url == f"http://{test_web_address}/"
    user_tag = page.locator(".navbar-nav :nth-child(1) .nav-link")
    sign_out_tag = page.locator(".navbar-nav :nth-child(2) .nav-link")
    expect(user_tag).to_have_text("Sign In")
    expect(sign_out_tag).to_have_text("Create Account")

"""
When you click on a listing of the index page, it should redirect you to said listing
"""
def test_listing_redirection_on_index(page, test_web_address, db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    page.goto(f"http://{test_web_address}/")
    # page.click(".image-container :nth-child(1) :nth-child(1)") <-- alternative syntax to below
    page.click(".image-container .listing-container a[href='/space/1']")
    assert page.url == f"http://{test_web_address}/space/1"



def test_page_has_loaded_images(page, test_web_address, db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    page.goto(f"http://{test_web_address}/")
    page.screenshot(path="images.png")
    
    # image_selector = "a[href='/space/1']" <-- alternative syntax to below
    image_selector1 = "img[src='static//images/oakhaven.png']" 
    image_selector2 = "img[src='static//images/stonegate.png']"
    image_selector3 = "img[src='static//images/glassvista.png']"
    image_selector4 = "img[src='static//images/hillsidelodge.png']"
    image_selector5 = "img[src='static//images/alpineoasis.png']"
    image_selector6 = "img[src='static//images/stoneserenity.png']"
    image_selector7 = "img[src='static//images/gardenviewhaven.png']"

    page.wait_for_selector(image_selector1)
    page.wait_for_selector(image_selector2)
    page.wait_for_selector(image_selector3)
    page.wait_for_selector(image_selector4)
    page.wait_for_selector(image_selector5)
    page.wait_for_selector(image_selector6)
    page.wait_for_selector(image_selector7)

    
    assert page.is_visible(image_selector1) 
    assert page.is_visible(image_selector2) 
    assert page.is_visible(image_selector3)
    assert page.is_visible(image_selector4) 
    assert page.is_visible(image_selector5)
    assert page.is_visible(image_selector6)
    assert page.is_visible(image_selector7)