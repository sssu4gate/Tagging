import pymongo 
import re


conn = pymongo.MongoClient('mongodb://scsc0511:483516729go1!@127.0.0.1')
crawling_db = conn.crawling_db
crawling_collection = crawling_db.crawling_collection
labels = ['자연 속에서 데이트', '기념일에 가기 좋은 데이트','트렌디한 데이트', '가성비 좋은 데이트', '고급스러운 데이트', '분위기 좋은 데이트']
label_to_write = ['nature','memorial','trendy','efficient','high','atmos']
f = open('../../data/blog.refined.tsv', 'w')
len_blog = 0

for i,label in enumerate(labels) :
  print('='*200)
  print(label)
  crawled_blogs = crawling_collection.find({'label':label})

  print(crawled_blogs)
  for blog in crawled_blogs :
    if len(blog['text']) <= 300 :
      continue
    len_blog += 1
    print('%d url : %s'%(len_blog,blog['url']))
    blog_text = blog['text'][100:]

    # 불필요한 공백 문자 제거
    replace_tab = blog_text.replace('\t','')
    replace_enter =blog_text.replace('\n','')
    replace_sp = replace_enter.replace('\u200b','')
    
    # 네이버 블로그에서 불필요한 뒤의 데이터 제거
    if blog['url'].find('naver') > 0 :
      pat = re.compile("북마크.*|블로그앱.*")
      to_store = replace_sp
      search_result = pat.search(replace_sp)
      
      if search_result != None :
        start_to_del = search_result.span()[0]
        to_store = label_to_write[i]+'\t'+replace_sp[:start_to_del]
      else :
        to_store = label_to_write[i] + '\t'+replace_sp
    else :
      to_store = label_to_write[i]+'\t'+replace_sp
    
    f.write(to_store+'\n')


f.close()
