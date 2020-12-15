from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException


class DaumCrawler() :
  def __init__(self, browser) :
    self.browser = browser

    if browser == 'chrome' :
      chrome_options = webdriver.ChromeOptions()
      chrome_options.add_argument('--headless')
      chrome_options.add_argument('--no-sandbox')
      chrome_options.add_argument('--disable-dev-shm-usage')
      self.driver = webdriver.Chrome('chromedriver',options=chrome_options)

  def tokenize_url(self, url) :
    url_tokens = url.split('?')
    base_url = url_tokens[0] + '?'
    
    param_tokens = url_tokens[1].split('&')[1:]
    params = dict()
    for param_token in param_tokens :
      param_name = param_token.split('=')[0]
      param_value = param_token.split('=')[1]
      params[param_name] = param_value

    return (base_url, params)

  def make_url(self,w, q, page) :
    base_url = 'https://search.daum.net/search?'
    
    q = q.replace(' ','+')
    q = str(q.encode('utf-8')).upper()
    q = q.replace('\\X','%')
    q = q[2:-1]

    w = 'w=' + w
    q = 'q=' + q
    page = 'page=' +str(page)

    daum_url = '&'.join([base_url, w, q, page])

    return daum_url
    
  def construct_url(self, base_url, params) :
    cur_url = base_url
    for param, value in params.items() :
      cur_url = cur_url + '&' +param + '=' + value

    return cur_url  

  def crawl_blog_addr(self, base_url, params) :
    blog_urls_list = list()
    cur_url = self.construct_url(base_url, params)
    print(cur_url)
    
    self.driver.get(cur_url)
    r = self.driver.page_source
    soup = BeautifulSoup(r, 'html.parser')
    blog_anchors = soup.select('a.f_link_b')
    blog_urls_list = [ anchor.get('href') for anchor in blog_anchors]  
    
    return blog_urls_list       

  def crawl_blog_addrs_part(self, base_url, params, page_num) :
    blog_urls_list = list()

    for i in range(0,page_num) :
      params['page'] = str(i+1)
      blog_urls = self.crawl_blog_addr(base_url, params)
      blog_urls_unique = [ url for url in blog_urls if url not in blog_urls_list] 
      
      blog_urls_list.extend(blog_urls_unique)

    return blog_urls_list  

  def crawl_blog_addrs_all(self, base_url, params) : 
    blog_urls_list = list()
    page_num = int(params['page'])
    while True:
      params['page'] = str(page_num)
      blog_urls = self.crawl_blog_addr(base_url, params)
      blog_urls_unique = [ url for url in blog_urls if url not in blog_urls_list] 
      if len(blog_urls_unique) == 0 :
        break;

      blog_urls_list.extend(blog_urls_unique)
      page_num += 1

    return blog_urls_list
      
  def crawl_blog_addrs(self, base_url, params) :
    page = 1

    if 'page_num' in params.keys() :
      page_num = params['page_num']
      del params['page_num']
    else :
      page_num = 1  


    blog_urls_list = list()

    print('='*100)
    print('blog url 크롤링 시작')
    ##page_num개의 page의 blog의 url 읽어오기
    if page_num >= 0 :
      blog_urls_list = self.crawl_blog_addrs_part(base_url, params, page_num)
    ##모든 page의 blog의 url 읽어오기
    else :
      blog_urls_list = self.crawl_blog_addrs_all(base_url, params)

    return blog_urls_list


  def crawl_blog_text(self, blog_urls_list,label) :
    blog_contents_dict = dict() 
    blog_contents_list = list()
    page_not_exist = False;
    

    print('='*100);
    print('블로그 텍스트 크롤링 시작')
    
    for blog_url in blog_urls_list :
      try :
        page_not_exist = True;
        self.driver.get(blog_url)
        self.driver.implicitly_wait(1)
        print(blog_url)
        iframes = self.driver.find_elements_by_tag_name('iframe')
        iframe_names = list()
        if len(iframes) > 0 :
          for iframe in iframes :
            try :
              iframe_name = iframe.get_attribute('name')
              if len(iframe_name) > 0 :
                iframe_names.append(iframe_name)
            except StaleElementReferenceException as e:
              print(e.__dict__['msg'])
              continue
      except TimeoutException as e:
        print(e.__dict__['msg'])
        continue
      except UnexpectedAlertPresentException as e :
        print(e.__dict__['msg'])
        result = self.driver.switch_to_alert()
        result.dismiss()
        continue

      if 'mainFrame' in iframe_names :
        self.driver.switch_to.frame("mainFrame")
      r = self.driver.page_source
      soup = BeautifulSoup(r, "html.parser")

      ##blog_tags =soup.select('p span')
      blog_tags =soup.select('p')
      
      blog_contents = [blog_tag.text for blog_tag in blog_tags]
      blog_contents = " ".join(blog_contents)
      blog_contents_dict[blog_url] = blog_contents
      cur_blog_contents = dict()
      cur_blog_contents['url'] = blog_url
      cur_blog_contents['text'] = blog_contents
      cur_blog_contents['label'] = label    
      blog_contents_list.append(cur_blog_contents) 
      print(len(blog_contents_list))
    return blog_contents_list   
