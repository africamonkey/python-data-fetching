# 4.1 抓取微博评论

针对一条微博（weiboId），抓取它底下的所有评论

# 4.2 批量抓取微博评论

weiboIds.csv 下有多条 weiboId ，自动抓取上述 weiboId 下的所有评论，生成任务列表allNeed.csv，将完成的写入completed.csv，将评论其保存到 content.csv

# 4.3 词频分析

从 content.csv 中读取数据，生成一张图片
