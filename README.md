## notificaciones_sunat

### Settings to allow background executions in Linux
```
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
```

### Script to install chromium and chromedriver
```
# Install Chromium browser
sudo apt-get update
sudo apt-get install -y chromium-browser

# Install ChromeDriver
sudo apt-get install -y chromium-chromedriver

# First install pip if you haven't already
sudo apt-get install python3-pip  # For Ubuntu/Debian
```

### Alternative approach using Python's webdriver-manager
```
# First install pip if you haven't already
sudo apt-get install python3-pip  # For Ubuntu/Debian

# Then install selenium and webdriver-manager
pip install selenium webdriver-manager

# Make ChromeDriver executable
sudo chmod +x /usr/bin/chromedriver

# Check ChromeDriver version
chromedriver --version
```

### Remember to also install the required dependencies:
```
# For Ubuntu/Debian
sudo apt-get install -y \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    default-jdk
```