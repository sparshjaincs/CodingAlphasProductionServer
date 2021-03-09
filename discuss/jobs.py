import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time

        

class Hiring:
    def __init__(self):
        pass
    
    def instance(self):
        url = "https://www.indeed.co.in/companies?from=gnav-homepage"
        data = requests.get(url)
        content = data.content
        soup = bs(content,'html.parser')
        return soup
    def get_data(self,instance):
        df ={}
        soup = instance.find('div',class_="cmp-PopularCompaniesWidget-companyName")
        img = instance.find('img')
        link = instance.find('a')
        if soup and img:
            df['name'] = soup.text.strip()
            df['logo'] = img['src']
            df['link'] = "https://in.indeed.com"+link['href']+'/jobs'
            
        return df
            
    def getinfo(self):
        soup = self.instance()
        soup = soup.find_all('div',class_="icl-Grid-col")
        
        df = []
        for ins in soup:
            name = self.get_data(ins)
            if name:
                df.append(name)
            
            
        return df
        
    
    def extract(self):
        data = self.getinfo()
        return data


class Indeed:
    def __init__(self,keyword,location,frompage,start):
        self.jobs = keyword
        self.location = location
        self.frompage = 'last'
        self.start = start
    def load_indeed(self):
        if self.start == 0:
            url = f"https://www.indeed.co.in/jobs?q={self.jobs}&l={self.location}&fromage={self.frompage}"
        else:
            url = f"https://www.indeed.co.in/jobs?q={self.jobs}&l={self.location}&fromage={self.frompage}&start={self.start}"
            
        data = requests.get(url)
        data = data.content
        soup = bs(data,"html.parser")
        job_soup = soup.find(id="resultsCol")
        return job_soup
    def indeed_title(self,element):
        try:
            title_elem = element.find('h2', class_='title')
            title = title_elem.text.strip()
        except:
            title = ""
        return title
    def indeed_summary(self,element):
        try:
            summary = element.find('div',class_ = 'summary')
            summary = summary.text
        except:
            summary = ""
        return summary
    def extract_company_indeed(self,job_elem,loca):
        db = {}
        try:
            company_elem = job_elem.find('div', class_='sjcl')
            company_data = company_elem.find('span',class_ = 'company')
            company = company_data.text.strip()
        except:
            company = ""
            
        try:
            location_data = company_elem.find('span',class_ = 'location')
            location = location_data.text.strip()
        except:
            location=loca.capitalize()
        #remote_data = company_elem.find('span',class_ = 'remote')
        #remote = remote_data.text.strip()
        #req_data = company_elem.find('div',class_='summary')
        #req = req_data.text.strip()
        
        
        db['company'] = company
        db['location'] = location
        #db['requirement'] = req_data
        #db['method'] = remote
        return db

    def extract_link_indeed(self,job_elem):
        link = job_elem.find('a')['href']
        link = 'https://www.indeed.co.in' + link
        return link
    def extract_requirement(self,element):
        #req_elem = element.find('div', class_='jobCardReqContainer')
        try:
            data = element.find('div',class_ = 'jobCardReqList')
            sol = ""
            for i in data.find_all('div',class_='jobCardReqItem'):
                sol += i.text.strip() + '\n'
            
        except:
            sol = ""
        #req = req_elem.text.strip()
        return sol
    def extract_date_indeed(self,job_elem):
        try:
            date_elem = job_elem.find('span', class_='date')
            date = date_elem.text.strip()
        except:
            date=""
        return date
    
    
    def extract_salary(self,element):
        try:
            salary = element.find('span',class_="salaryText")
            salary = salary.text.strip()
        except:
            salary = ""
        return salary
    def get_indeed_job_data(self):
        db = list()
        instance = self.load_indeed()
        data = instance.find_all('div', class_='jobsearch-SerpJobCard')
        for x in data:
            try:
                sol = dict()
                title = self.indeed_title(x)
                company = self.extract_company_indeed(x,self.location)
                link = self.extract_link_indeed(x)
                date = self.extract_date_indeed(x)
                summary = self.indeed_summary(x)
                req = self.extract_requirement(x)
                salary = self.extract_salary(x)
                sol['title'] = title
                sol['company'] = company
                sol['link'] = link
                sol['date'] = date
                sol['summary'] = summary
                sol['requirement'] = req
                sol['salary'] = salary
                sol['jobs'] = 'Full Time'
                db.append(sol)
            except:
                pass
        return db
    def extract(self):
        soup = self.get_indeed_job_data()
        return soup
        

class Monster:
    def __init__(self,designation,location,start=0,limit=25,sort=1):
        self.desig = designation
        self.location = location
        self.limit = limit
        self.sort = sort
        self.start = start
    def get_link(self):
        link = f'https://www.monsterindia.com/srp/results?start={self.start}&sort={self.sort}&limit={self.limit}&query={self.desig}&locations={self.location}'
        return link
    def get_instance(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe",options=options)
        driver.get(self.get_link())
        soup = bs(driver.page_source,'html5lib')
        driver.close()
        return soup
    def extract(self):
        data = []
        soup = self.get_instance()
        element = soup.find_all('div', class_="card-panel apply-panel job-apply-card")
        for job in element:
            try:
                d = {}
                d['title'] = job.find('div',class_="job-tittle").find('a').text
                d['link'] = job.find('div',class_="job-tittle").find('a').get('href')
                d['company'] = {'company':job.find('span',class_="company-name").text,'location':self.location}
                data1 = job.find('div',class_="searctag row").find_all('span',class_="loc")
                if len(data1)>2:
                    d['experience'] = data1[1].text
                    d['salary'] = data1[2].text
                else:
                    d['experience'] = data1[1].text
                    d['salary'] = 'Not Disclosed'
                d['summary'] = job.find('p',class_="job-descrip").text
                try:
                    tags = job.find('p',class_="descrip-skills").find_all('span',class_="grey-link")
                    l = []
                    for i in tags:
                        l.append(i.text.strip().rstrip(","))
                except:
                    l=[]
                    
                    
                d['tags'] = l
                d['date']=job.find('span',class_="posted").text
                d['jobs']='Full Time'
                data.append(d)
            except:
                pass
        return data     
class Naukri:
    def __init__(self,designation,location,page):
        self.desig = designation
        self.city = location
        self.page = page
        
    def get_link(self):
        if self.desig and self.city is None:
            link = f'https://www.naukri.com/{self.desig}-jobs-{self.page}'
        elif self.city and self.desig is None:
            link = f"https://www.naukri.com/jobs-in-{self.city}-{self.page}"
        else:
            link = f'https://www.naukri.com/{self.desig}-jobs-in-{self.city}-{self.page}'
        return link
    
    def get_instance(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe",options=options)
        driver.get(self.get_link())
        soup = bs(driver.page_source,'html5lib')
        driver.close()
        return soup
    
    def extract(self):
        soup = self.get_instance()
        results = soup.find(class_='list')
        job_elems = results.find_all('article',class_='jobTuple bgWhite br4 mb-8')
        data=[]
        for job in job_elems:
            try:
                d = {
                    'link':job.find('a',class_="title fw500 ellipsis").get('href'),
                    'title':job.find('a',class_="title fw500 ellipsis").text,
                    'company':{'company':job.find('a',class_="subTitle").text,'location':self.city},
                    'experience':job.find('li',class_="experience").text,
                    'salary':job.find('li',class_="salary").text,
                    'summary':job.find('div',class_="job-description").text,
                    'date':job.find('div',class_="jobTupleFooter").find_all('span')[1].text,
                    'jobs':'Full Time'
                }
                tags = job.find('ul',class_="tags has-description")
                l = []
                for i in tags.find_all('li'):
                    l.append(i.text)
                d['tags'] = l
                rating = job.find('span',class_="starRating fleft dot")
                if rating is None:
                    rate = ""
                else:
                    rate = rating.text
                d['rating'] = rate
                review = job.find('a',class_="reviewsCount")
                if review is None:
                    Rev = ""
                else:
                    Rev = review.text
                d['review'] = Rev
                data.append(d)
            except:
                pass
        return data
        
        
        
class Jobs(Indeed,Monster,Naukri):
    '''
    Jobs(keyword,location,page)
    '''
    def __init__(self,keyword,location,page):
        self.keyword = keyword
        self.location = location
        self.page = page
    def indeed(self,start):
        i1 = Indeed(self.keyword,self.location,'last',start)
        i2 = Indeed(self.keyword,self.location,'last',start+10)
        return i1.extract() + i2.extract()
    def monster(self,start):
        i1 = Monster(self.keyword,self.location,start)
        return i1.extract()
    def naukri(self,page):
        i1 = Naukri(self.keyword,self.location,page)
        return i1.extract()
        
        
    def select(self):
        if self.page == 1:
            return self.indeed(0)
        elif self.page == 2:
            return self.indeed(20)
        elif self.page == 3:
            return self.monster(0)
        elif self.page == 4:
            return self.monster(25)
        elif self.page == 5:
            return self.indeed(40)
        elif self.page==6:
            return self.naukri(1)
        elif self.page == 7:
            return self.naukri(2)
        elif self.page == 8:
            return self.indeed(60)
        elif self.page == 9:
            return self.monster(50)
        elif self.page == 10:
            return self.naukri(3)
            
            
        
        
        