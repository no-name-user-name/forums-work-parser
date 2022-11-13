import os
import undetected_chromedriver as uc


def start_driver(profile, is_headless:bool = True, wait_time:float=5):
    temp_dir_path = os.getcwd() + '/_temp/' + 'profile_' + str(profile)
    os.makedirs(temp_dir_path, exist_ok=True)

    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.page_load_strategy = 'eager'

    if is_headless:
        options.add_argument('--headless')

    driver = uc.Chrome(options=options, user_data_dir=temp_dir_path)
    driver.implicitly_wait(wait_time)
    return driver