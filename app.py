from pwinput import pwinput as pw
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from warnings import filterwarnings
filterwarnings('ignore')


## Input Username and Password
username = input("Enter Username : ")
password = pw(prompt="Enter Password : ",mask="*")
print()

loginLink = 'https://lms.snuchennai.edu.in/login/index.php'

## Initialise driver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)                             ## Prevent chrome from auto-closing on program termination
options.add_experimental_option('excludeSwitches', ['enable-logging'])      ## Hide 'DevTools Listening on ws://...'
driver=webdriver.Chrome(options=options)

## Load LMS webpage
driver.get(loginLink)

## Login to LMS
userxpath='//*[@id="username"]'
pwdxpath='//*[@id="password"]'
SendUsername = driver.find_element(by=By.XPATH,value=userxpath).send_keys(username)
SendPassword = driver.find_element(by=By.XPATH,value=pwdxpath).send_keys(password + Keys.ENTER)


## Load the Courses Overview webpage
CourseOverviewLink = "https://lms.snuchennai.edu.in/grade/report/overview/index.php"
driver.get(CourseOverviewLink)

## Find the Course Overview <table> element
CourseOverviewTable = driver.find_element(by=By.XPATH,value='//*[@id="overview-grade"]')

## LIST: List of hrefs from <table>
LIST=[]

## Iterate through rows of <table>, extract href from each row's <td> cell 0
flag=True
for row in CourseOverviewTable.find_elements(by=By.XPATH,value='.//tr'):
    if flag:
        flag=False
        continue
    coursename=row.find_element(by=By.XPATH,value='.//td')
    try:
        course = coursename.find_element(by=By.TAG_NAME,value='a')
        courselink = course.get_attribute('href')
        LIST.append(courselink)
    except Exception:
        pass
    

## Load each webpage from the list of hrefs, and check if an 'Attendance' href is present in it
## If yes, store it in AttendanceLink
for link in LIST:
    driver.get(link)
    if 'Attendance' in driver.find_element(by=By.XPATH,value="/html/body").text: 
        tag = driver.find_elements(by=By.TAG_NAME,value='a')
        for i in range(len(tag)):
            if 'attendance' in tag[i].get_attribute('href'):
                AttendanceLink = tag[i].get_attribute('href')
                break
        break

## Append '&mode=1' to the AttendanceLink to load the 'All Courses' webpage
driver.get(AttendanceLink+'&mode=1')
    

## AttendanceData: Dictionary - keys: course names; values: list of attendance details
AttendanceData={}

## Iterate through <table> element in the 'All Courses' webpage to get AttendanceData
AttendanceTable = driver.find_element(by=By.XPATH,value='//*[@id="region-main"]/div[1]/table[1]')
flag2=True
for row in AttendanceTable.find_elements(by=By.XPATH,value=".//tr"):
    if flag2:
        flag2=False
        continue
    data=[td.text for td in row.find_elements(by=By.XPATH,value=".//td")]
    AttendanceData[data[0]]=data[2:]
del AttendanceData['Average attendance']

## Display AttendanceData
for subject in AttendanceData:
    try:
        total = int(AttendanceData[subject][0])
        AttendancePercentage = float((AttendanceData[subject][2])[:-1])
        No_of_present = round(total * AttendancePercentage/100)
        print(subject)
        print('-'*(len(subject)+5))
        print('Present for :',No_of_present)
        print('Total Classes :',total)
        print('Attendance percentage : ',AttendancePercentage,'%',sep='')
        print('\n\n')
    except Exception:
        pass

#driver.close()
input('Press any key to exit...')
