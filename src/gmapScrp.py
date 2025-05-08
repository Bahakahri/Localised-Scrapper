
"""
def scrapData(driver,storetype,city,allowed_hexes):
    name = "PlaceHolder"
    seen_names = set()
    results = []
    
    searchbox = driver.find_element(By.ID,"searchboxinput")
    searchbox.clear()
    searchbox.send_keys(f"{storetype} near {city}")
    searchbox.send_keys(Keys.ENTER)
    scrollbar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@role, 'feed')]")))
    lastheight = driver.execute_script("return arguments[0].scrollHeight", scrollbar)
    print("Scrapping data ...")

    while True:

        elements = WebDriverWait(driver, 4).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class, 'Nv2PK')]")))

        for element in elements:

            try:

                url = element.find_element(By.XPATH, ".//a[contains(@class, 'hfpxzc')]").get_attribute("href")
                coords_match = re.search(r'!3d([0-9\.\-]+)!4d([0-9\.\-]+)', url)

                if not coords_match:
                    continue  # Skip if no coordinates

                lat = float(coords_match.group(1))
                lon = float(coords_match.group(2))
                h3_id = h3.latlng_to_cell(lat, lon, 8)

                if h3_id not in allowed_hexes:
                    continue  # Skip if outside allowed hexes

                name = element.find_element(By.XPATH,".//div[contains(@class, 'NrDZNb')]").text

                if name in seen_names:
                    continue  # Skip duplicates

                rating = element.find_element(By.XPATH, ".//div[contains(@class, 'AJB7ye')]").text
                c2 = element.find_elements(By.XPATH, ".//div[contains(@class, 'W4Efsd')]")
                c2desc = c2[1].text if len(c2) > 1 else ""

                stars = rating.split('(')[0]
                reviews = rating.split('(')[1].split(')')[0] if '(' in rating and ')' in rating else "0"
                parts = c2desc.split("·")
                store_type = parts[0].strip()
                address = parts[1].split("\n")[0].strip() if len(parts) > 1 else ""

                results.append({

                    'Store Name' : name,
                    'Address' : address,
                    'Type' : store_type,
                    'Rating' : stars,
                    'Reviews' : reviews,
                    'URL' : url
                })

                seen_names.add(name)

            except Exception as e:

                print(e)
                continue

            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollbar)
            time.sleep(2)
            newheight = driver.execute_script("return arguments[0].scrollHeight", scrollbar)

            if newheight == lastheight:
                break
            lastheight = newheight
    print("Done Successfully!")
    return(results)
"""


def scrapData(driver, storetype, city, allowed_hexes):
    import re
    import time
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import h3

    seen_names = set()
    results = []

    # Step 1: Search
    searchbox = driver.find_element(By.ID, "searchboxinput")
    searchbox.clear()
    searchbox.send_keys(f"{storetype} near {city}")
    searchbox.send_keys(Keys.ENTER)

    # Step 2: Wait for results container
    try:
        scrollbar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@role, 'feed')]"))
        )
        print("Scrollbar found.")
    except Exception as e:
        print(f"Failed to find scrollbar: {e}")
 
    
    print("Scraping data ...")

    lastheight = driver.execute_script("return arguments[0].scrollHeight", scrollbar)
    scroll_attempts = 0

    while True:


        try:
            # Wait for visible result cards
            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'Nv2PK')]"))
            )
            print(f"Found {len(elements)} elements")
        except Exception as e:
            print(f"Error finding result cards: {e}")
            break

        for element in elements:
            try:
                url = element.find_element(By.XPATH, ".//a[contains(@class, 'hfpxzc')]").get_attribute("href")
                coords_match = re.search(r'!3d([0-9\.\-]+)!4d([0-9\.\-]+)', url)

                if not coords_match:
                    print("No coordinates found in URL")
                    continue

                lat = float(coords_match.group(1))
                lon = float(coords_match.group(2))
                h3_id = h3.latlng_to_cell(lat, lon, 8)

                if h3_id not in allowed_hexes:
                    print("Skipped due to hex exclusion")
                    continue

                name = element.find_element(By.XPATH, ".//div[contains(@class, 'NrDZNb')]").text
                if name in seen_names:
                    continue

                rating_element = element.find_elements(By.XPATH, ".//div[contains(@class, 'AJB7ye')]")
                rating = rating_element[0].text if rating_element else "0"
                c2 = element.find_elements(By.XPATH, ".//div[contains(@class, 'W4Efsd')]")
                c2desc = c2[1].text if len(c2) > 1 else ""

                stars = rating.split('(')[0].strip()
                reviews = rating.split('(')[1].split(')')[0] if '(' in rating and ')' in rating else "0"
                parts = c2desc.split("·")
                store_type = parts[0].strip()
                address = parts[1].split("\n")[0].strip() if len(parts) > 1 else ""

                results.append({
                    'Store Name': name,
                    'Address': address,
                    'Type': store_type,
                    'Rating': stars,
                    'Reviews': reviews,
                    'URL': url
                })

                seen_names.add(name)

            except Exception as e:
                print(f"Error parsing element: {e}")
                continue

        # Scroll down
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollbar)
        time.sleep(2)
        newheight = driver.execute_script("return arguments[0].scrollHeight", scrollbar)

        if newheight == lastheight:
            scroll_attempts += 1
            if scroll_attempts >= 2:  # try twice before breaking
                print("No more new content. Stopping.")
                break
        else:
            scroll_attempts = 0

        lastheight = newheight

    print("Done Successfully!")
    return results


