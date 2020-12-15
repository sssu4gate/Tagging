from daum_crawler import DaumCrawler
import pymongo

conn = pymongo.MongoClient('mongodb://127.0.0.1')
crawling_db = conn.crawling_db
crawling_collection = crawling_db.crawling_collection


tags = ['자연 속에서 데이트', '기념일에 가기 좋은 데이트', '트렌디한 데이트', '가성비 좋은 데이트', '고급스러운 데이트', '분위기 좋은 데이트']

#DesiredCapabilities capabilities = new DesiredCapabilities()
#capabilities.setCapability(CapabilityType.UNEXPECTED_ALERT_BEHAVIOUR, UnexpectedAlertBehaviour.ACCEPT)
#WebDriver driver = new ChromeDriver(capabilities);


daum_crawler = DaumCrawler('chrome')
for tag in tags :
  url = daum_crawler.make_url('blog',tag,1)
  base_url, params = daum_crawler.tokenize_url(url)
  params['page_num'] = -1
  blog_url = daum_crawler.crawl_blog_addrs(base_url, params)
  blog_text = daum_crawler.crawl_blog_text(blog_url,tag)
  print(tag)
  print(len(blog_text))
  crawling_collection.insert_many(blog_text)
  
  
