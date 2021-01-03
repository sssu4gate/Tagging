from daum_crawler import DaumCrawler
import pymongo


def filter_blog_urls(blog_urls, tag) :
   blog_urls_not_exist = list()
   for blog_url in blog_urls :
     if crawling_collection.count_documents({'url' : blog_url, 'label' : tag}) == 0 :
       blog_urls_not_exist.append(blog_url) 
   return blog_urls_not_exist


conn = pymongo.MongoClient('mongodb://127.0.0.1')
crawling_db = conn.crawling_db
crawling_collection = crawling_db.crawling_collection


tags = ['힐링되는 데이트', '트렌디한 데이트', '가성비 좋은 데이트','기념일에 가기 좋은', '고급스러운 데이트', '분위기 좋은 데이트']
keywords = [['힐링되는 데이트','힐링 데이트','자연 속 데이트', '자연 친화적 데이트', '식물 데이트', '동물 데이트', '자연 경관 데이트', '정원 데이트', '고즈넉한 데이트','전통적인 데이트', '고요한 데이트','한적한 데이트'],
[#'트렌디한 데이트','유행하는 데이트','모던한 데이트',
 '세련된 데이트','힙한 데이트','인싸 데이트', '개성있는 데이트','이색 데이트','특색 데이트','인스타 감성 데이트','핫플레이스 데이트'],
['가성비 좋은 데이트', '대박 싼 데이트', '저렴한 데이트', '가격 부담 없는 데이트', '착한 가격 데이트','소소한 데이트', '소박한 데이트', '가격 대비 만족 데이트','가격 대비 퀄리티 좋은 데이트','가성비 있는 데이트','가격이 착한 데이트'],
['기념일에 가기 좋은 데이트','특별한 날에 가기 좋은 데이트','100일 데이트','1년 데이트','결혼 기념일 데이트','발렌타인 데이 데이트','화이트 데이 데이트','의미있는 날 데이트','빼빼로 데이 데이트', '크리스마스 데이트'],
['고급스러운 데이트','럭셔리한 데이트','호텔 데이트','비싸지만 퀄리티있는 데이트','비싸지만 만족스러운 데이트', '비싸지만 가격 값 하는 데이트','호화로운 데이트','고상한 데이트', '세련된 데이트','우아한 데이트','품격있는 데이트','파인 다이닝 데이트', '품위 있는 데이트'],
['분위기 좋은 데이트','분위기 깡패 데이트','분위기 값 데이트','분위기 맛집 데이트','야경 데이트','근사한 데이트','아늑한 데이트','따뜻한 분위기 데이트','황홀한 데이트','가로수길 데이트']]

#DesiredCapabilities capabilities = new DesiredCapabilities()
#capabilities.setCapability(CapabilityType.UNEXPECTED_ALERT_BEHAVIOUR, UnexpectedAlertBehaviour.ACCEPT)
#WebDriver driver = new ChromeDriver(capabilities);


daum_crawler = DaumCrawler('chrome')
for i,tag in enumerate(tags) :
  print('TAG : %s'%tag)
  for keyword in keywords[i]:
    url = daum_crawler.make_url('blog',keyword,1)
    base_url, params = daum_crawler.tokenize_url(url)
    params['page_num'] = -1
    blog_urls = daum_crawler.crawl_blog_addrs(base_url, params)
    blog_urls = filter_blog_urls(blog_urls, tag)
    blog_texts = daum_crawler.crawl_blog_text(blog_urls,tag)
    print(keyword)
    print(len(blog_texts))
    crawling_collection.insert_many(blog_texts)
  
  
