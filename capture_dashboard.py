from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set Chrome to use the print to PDF feature
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--print-to-pdf-no-header")
chrome_options.add_argument(f"--print-to-pdf={os.path.join(os.getcwd(), 'dashboard.pdf')}")

# Set path to chromedriver as per your installation
chrome_driver_path = ChromeDriverManager().install()

# Set service
service = Service(chrome_driver_path)

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Go to your Streamlit app's URL
driver.get('http://localhost:8501')  # Replace with your Streamlit app's URL

# Wait for the page to load completely before printing to PDF
driver.implicitly_wait(10)

# Close the browser
driver.quit()
