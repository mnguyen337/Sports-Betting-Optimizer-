from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import time
import pandas as pd

############################################################################

driver = uc.Chrome()

###########################################################################


# Scraping PrizePicks
driver.get("https://app.prizepicks.com/")
time.sleep(3)

# Waiting and closes popup
WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "close")))
time.sleep(3)
driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div/div[3]/button").click()
time.sleep(3)

# Creating tables for players
ppPlayers = []

# change sport
driver.find_element(By.XPATH, "//div[@class='name'][normalize-space()='MLB']").click()
time.sleep(5)

# wait until stat container is viewable
stat_container = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "stat-container")))

# finding all stat elements
categories = driver.find_element(By.CSS_SELECTOR, ".stat-container").text.split('\n')

# Collecting categories
for category in categories:
    driver.find_element(By.XPATH, f"//div[text()='{category}']").click()

    projectionsPP = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".projection")))

    for projections in projectionsPP:
        names = projections.find_element(By.CLASS_NAME, "name").text
        value = projections.find_element(By.CLASS_NAME, "presale-score").get_attribute('innerHTML')
        proptype = projections.find_element(By.CLASS_NAME, "text").get_attribute('innerHTML')

        players = {
            'Name': names,
            'Prize Pick Value': value,
            'Prop': proptype.replace("<wbr>", "").replace("", "")
        }
        ppPlayers.append(players)

# change sport
driver.find_element(By.XPATH, "//div[@class='name'][normalize-space()='LoL']").click()
time.sleep(5)

# wait until stat container is viewable
stat_container = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "stat-container")))

# finding all stat elements
categories = driver.find_element(By.CSS_SELECTOR, ".stat-container").text.split('\n')

# Collecting categories
for category in categories:
    driver.find_element(By.XPATH, f"//div[text()='{category}']").click()

    projectionsPP = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".projection")))

    for projections in projectionsPP:
        names = projections.find_element(By.CLASS_NAME, "name").text
        value = projections.find_element(By.CLASS_NAME, "presale-score").get_attribute('innerHTML')
        proptype = projections.find_element(By.CLASS_NAME, "text").get_attribute('innerHTML')

        players = {
            'Name': names,
            'Prize Pick Value': value,
            'Prop': proptype.replace("<wbr>", "").replace(" ", "")
        }
        ppPlayers.append(players)

PrizeProps = pd.DataFrame(ppPlayers)

# Scraping Underdog
driver.get("https://underdogfantasy.com/pick-em/higher-lower")
time.sleep(3)
LogIn = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div/form/div[1]/label/div[2]/input')
LogIn.send_keys("mikenguyen475@gmail.com")
LogIn2 = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div/form/div[2]/label/div[2]/input")
LogIn2.send_keys("Mn@200413196")
LogIn.send_keys(Keys.RETURN)
time.sleep(10)
underdogplayers = []
driver.find_element(By.XPATH, "//p[@class='styles__text__e2zTE styles__pickEmText__rjhzq'][normalize-space()='Basketball']").click()
time.sleep(5)
playersdata = driver.find_elements(By.CLASS_NAME, 'styles__overUnderCell__KgzNn')
for player in playersdata:
    name = player.find_element(By.CLASS_NAME, 'styles__playerName__jW6mb').text
    stats= player.find_elements(By.CLASS_NAME, 'styles__topHalf__gguxy')
    for stat in stats:
        stat = stat.text
        players = {
            'Name': name,
            'Underdog Value': stat[:4],
            'Prop': stat[4:]
        }
        underdogplayers.append(players)


driver.find_element(By.XPATH, "//p[@class='styles__text__e2zTE styles__pickEmText__rjhzq'][normalize-space()='Esports']").click()
time.sleep(5)
playersdata = driver.find_elements(By.CLASS_NAME, 'styles__overUnderCell__KgzNn')
for player in playersdata:
    name = player.find_element(By.CLASS_NAME, 'styles__playerName__jW6mb').text
    stats= player.find_elements(By.CLASS_NAME, 'styles__topHalf__gguxy')
    for stat in stats:
        stat = stat.text
        players = {
            'Name': name,
            'Underdog Value': stat[:4],
            'Prop': stat[4:]
        }
        underdogplayers.append(players)
UnderdogProps = pd.DataFrame(underdogplayers)
UnderdogProps.to_csv('Test1.csv')
PrizeProps.to_csv('Test2.csv')
# column_mapping = {}
# for value1 in PrizeProps['Prop']:
#     # Find the best match for each value from df1['Prop'] in df2['Prop']
#     match = process.extractOne(value1, UnderdogProps['Prop'], scorer=fuzz.ratio)
#     # If the match has a similarity score above a certain threshold, consider it a match
#     if match[1] > 60:  # Adjust the threshold as per your requirements
#         # Map the value from df1 to the corresponding value in df2
#         column_mapping[value1] = match[0]
#
# # Create a new column 'MappedProp' in df1 with the mapped values from column_mapping
# PrizeProps['MappedProp'] = PrizeProps['Prop'].map(column_mapping)
#
# # Perform the merge based on the 'Name' and 'MappedProp' columns
# merged_df = pd.merge(PrizeProps, UnderdogProps, left_on=['Name', 'MappedProp'], right_on=['Name', 'Prop'], how='inner')
# # Drop the additional columns used for mapping
# merged_df.drop(columns=['MappedProp', 'Prop_y'], inplace=True)
# merged_df.to_csv('test3.csv')











