from modules.selenium_wrapper import SeleniumWrapper
import os
from selenium.webdriver.common.keys import Keys


class OLX():
    def __init__(self) -> None:
        self.se = SeleniumWrapper()
        self.se.setup_driver(
            headless=False, profile=r'C:\Users\mypc0\AppData\Local\Google\Chrome\User Data\Profile 1')
        self.se.get_page('https://www.olx.ro/')

        # Accept cookies
        self.se.find_element('#onetrust-accept-btn-handler', timeout=5,
                             click=True, print_error=False)
        self.se.wait_random_time(2, 3)
        
    def select_olx_dropdown(self, index: int, value: str) -> None:
        dropdown = self.se.find_elements('div[class="css-46mz1a"]')[index]
        self.se.find_element(
            selector='button[data-testid="dropdown-expand-button"]',
            parent=dropdown,
            click=True
        )
        self.se.wait_random_time(b=1)
        options = self.se.find_elements(
            selector='li[data-testid="dropdown-item"]',
            parent=dropdown,
        )
        value = str(value).strip().lower()
        for option in options:
            if option.text.strip().lower() == value:
                option.click()
                return

    def login(self, username: str, password: str) -> bool:
        is_logged_in_selector = 'a[href="/d/myaccount"]'

        if self.se.is_logged_in(is_logged_in_selector):
            print('Already logged in')
            return True
        else:
            self.se.find_element('a[data-cy="myolx-link"]', click=True)
            self.se.wait_random_time(3, 4)

            assert self.se.driver.current_url.startswith(
                'https://ro.login.olx.com'), 'Not on the login page'

            self.se.element_send_keys(
                text=username,
                selector='input[name="username"]'
            )
            self.se.element_send_keys(
                text=password,
                selector='input[name="password"]'
            )
            self.se.wait_random_time(2, 3)

            self.se.find_element(
                selector='button[data-testid="login-submit-button"]', click=True)

            self.se.wait_random_time(10, 12)

            is_success = self.se.is_logged_in(is_logged_in_selector)
            print(f'Logged in {username}' if is_success else f'Failed to login {username}')
            return is_success

    def post_item(self, item: dict) -> None:
        self.se.find_element('a[data-cy="post-new-ad-button"]', click=True)
        self.se.wait_random_time(3, 4)

        # Popup
        popup = self.se.find_element(
            selector='div[aria-label="Nexus Modal"]',
            timeout=5,
            print_error=False,
        )
        if popup:
            self.se.find_element(
                selector='span.css-1ohf0ui',
                parent=popup,
                click=True
            )
            self.se.wait_random_time(2, 3)

        # Title
        self.se.element_send_keys(
            text=item['Title'],
            selector='#title'
        )
        self.se.wait_random_time(1, 2)

        # Images
        for img in os.listdir(item['Images']):
            path = os.path.join(os.getcwd(), item['Images'], img)
            file_input = self.se.driver.execute_script(
                """
                return document.querySelector('input[data-testid="attach-photos-input"]');
                """
            )
            file_input.send_keys(path)
            self.se.wait_random_time(3, 4)

        # Pret / Price
        self.se.element_send_keys(
            text=str(item['Price']),
            selector='input[data-testid="price-input"]'
        )

        # Currency
        self.select_olx_dropdown(0, '€')
        self.se.wait_random_time()
        
        # negociabil / negotiable
        self.se.find_element(
            selector='div[aria-label="Negociabil"]',
            click=True
        )
        self.se.wait_random_time()

        # Model
        self.select_olx_dropdown(1, item['Model'])
        self.se.wait_random_time(1, 2)

        # Capacitate Motor
        self.se.element_send_keys(
            text=str(item['Motor']),
            selector='input[data-cy="parameters.enginesize"]'
        )
        self.se.wait_random_time(b=0.4)

        # Putere / Power
        self.se.element_send_keys(
            text=str(item['Power']),
            selector='input[data-cy="parameters.engine_power"]'
        )
        self.se.wait_random_time(b=0.4)

        # Combustibil / Fuel type
        self.select_olx_dropdown(2, item['Fuel type'])
        self.se.wait_random_time(1, 2)

        # Caroserie / Body type
        self.select_olx_dropdown(3, item['Body type'])
        self.se.wait_random_time(1, 2)

        # Rulaj / Mileage
        self.se.element_send_keys(
            text=str(item['Mileage']),
            selector='input[data-cy="parameters.rulaj_pana"]'
        )
        self.se.wait_random_time(b=0.4)

        # Culoare / Color
        self.select_olx_dropdown(4, item['Color'])
        self.se.wait_random_time(1, 2)

        # An de fabricatie / Year
        self.se.element_send_keys(
            text=str(item['Year']),
            selector='input[data-cy="parameters.year"]'
        )
        self.se.wait_random_time(b=0.4)

        # Numar de usi / Doors
        self.select_olx_dropdown(5, str(item['Doors']))
        self.se.wait_random_time(1, 2)

        # Stare / Shape
        self.se.find_element(
            selector='div[title="{}"] button'.format(
                item['Shape'].strip().capitalize()),
            click=True
        )
        self.se.wait_random_time(b=0.4)

        # Cutie de viteze / Gear
        self.se.find_element(
            selector='div[title="{}"] button'.format(
                item['Gear'].strip().capitalize()),
            click=True
        )
        self.se.wait_random_time(b=0.4)

        # Volan / Wheel side
        self.se.find_element(
            selector='div[title="{}"]'.format(
                item['Wheel side'].strip().capitalize()),
            click=True
        )
        self.se.wait_random_time(b=0.4)

        # Inmatriculat/Neinmatriculat / Registered/Unregistered
        self.se.find_element(
            selector='div[title="{}"]'.format(
                item['Registered'].strip().capitalize()),
            click=True
        )
        self.se.wait_random_time(b=0.4)
        
        # Descriere / Description
        textarea = self.se.driver.execute_script(
            """
            const textarea = document.getElementById("description");
            textarea.textContent = arguments[0];
            return textarea;
            """,
            str(item['Description'])
        )
        self.se.element_click(textarea)
        textarea.send_keys(Keys.SPACE)
        textarea.send_keys(Keys.TAB)
        self.se.wait_random_time(1, 2)
        
        # Localitate / City
        self.se.driver.execute_script(
            'document.querySelector("input[name=city_id]").value = arguments[0];',
            item['City']
        )
        self.se.wait_random_time(1, 2)
        
        # Nume / Name
        
        # Numarul de telefon / Phone number
        self.se.element_send_keys(
            text=str(item['Phone number']),
            selector='#phone'
        )
        self.se.wait_random_time(b=0.4)

        # Submit Button
        self.se.find_element(
            selector='button[data-testid="submit-btn"]',
            click=True
        )
        self.se.wait_random_time(5, 6)
        
        # Continue without promotion / Continua fara promovare
        self.se.find_element(
            selector='button.css-18l8bp6',
            click=True
        )
        self.se.wait_random_time(2, 3)
        
        # Success
        is_success = self.se.find_element(
            selector='img[alt="success"]',
            print_error=False
        )
        
        # Go to the first page
        self.se.find_element(
            selector='.css-1bgiaj0',
            click=True,
            print_error=False
        )
        self.se.wait_random_time(2, 3)
        
        print('Item posting success: Anunțul tău a fost activat' if is_success else 'Failed to post item')
        
        
    def uncheck_view_profile(self) -> None:
        self.se.get_page('https://www.olx.ro/myaccount/profile/')
        self.se.wait_random_time(3, 4)
        
        # Edit profile
        self.se.find_element(
            selector='button[data-cy="user-profile-edit-button"]',
            click=True
        )
        
        # Permite utilizatorilor să îți vadă profilul / Allow users to view your profile
        checkbox = self.se.find_element(
            selector='div[aria-label="Permite utilizatorilor să îți vadă profilul"]',
        )
        assert checkbox, 'Permite utilizatorilor să îți vadă profilul checkbox not found'
        if checkbox.get_attribute('aria-checked') == 'true':
            self.se.element_click(checkbox)
    
        # Save
        self.se.find_element(
            selector='button.css-165srwn',
            click=True
        )
        
        