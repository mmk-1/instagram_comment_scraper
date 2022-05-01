from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from post import Post
import time
import sys

if(len(sys.argv) <= 3):
    print("Need all arguments to run!")
    print("Run in this format: py main.py username password scraping_username")
    sys.exit(1)


driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
driver.get("https://www.instagram.com/")



# login
time.sleep(3)
username=driver.find_element(By.NAME, "username")
password=driver.find_element(By.CSS_SELECTOR, "input[name='password']")
username.clear()
password.clear()
username.send_keys(sys.argv[1]) # Username
password.send_keys(sys.argv[2]) # Password
# login = driver.find_element_by_css_selector("button[type='submit']").click()
login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(5)
notnow = driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
# notnow = driver.find_element(By.XPATH, '//button[contains(text(), "Not Now")]')
time.sleep(5)
# notnow = driver.find_element(By.XPATH, '//button[contains(text(), "Not Now")]')
try:
    notnow2 = driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
    time.sleep(2)
except Exception as e:
    print(e)
    pass

#searchbox
searchbox=driver.find_element_by_css_selector("input[placeholder='Search']")
searchbox.clear()
searchbox.send_keys(sys.argv[3]) # Username to be scraped
time.sleep(2)
searchbox.send_keys(Keys.ENTER)
time.sleep(2)
searchbox.send_keys(Keys.ENTER)
time.sleep(2)

#scroll
posts = []
final_posts = []
links = driver.find_elements(By.TAG_NAME, 'a')
# print(links)
for link in links:
    post = link.get_attribute('href')
    if '/p/' in post:
        posts.append(post)

# comments = []
if len(posts) > 5:
    posts = posts[:5]
# print(posts)
# print('\n'*4)
time.sleep(1.5)

# comments = []
for post in posts:
    newPost = Post(post)
    thePost = driver.get(post)
    comments = driver.find_elements(By.CLASS_NAME, 'Mr508')
    for c in comments:
        container = c.find_element_by_class_name('C4VMK')
        name = container.find_element(By.CLASS_NAME, '_6lAjh').text
        contentContainer = container.find_element(By.CLASS_NAME, 'MOdxS')
        commentItself = contentContainer.find_element(By.TAG_NAME, 'span').text
        newPost.addComment(name, commentItself)
    final_posts.append(newPost)
    time.sleep(2)


with open("out.txt", "w", encoding='utf_8') as f:
    for post in final_posts:
        f.write(post.url + '\n')
        for key in post.comments.keys():
            f.write('user:' + key + '\n')
            f.write('comment:' + post.comments[key] + '\n')
            # f.write(newPost.comments])
        f.write('______________________________________'+ '\n'*3)


# scrolldown=driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
# match=False
# while(match==False):
#     last_count = scrolldown
#     time.sleep(3)
#     scrolldown = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
#     if last_count==scrolldown:
#         match=True

