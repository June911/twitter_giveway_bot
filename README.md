## 推特白名单机器人

1. 写个每天发gm 的机器人
2. 获取首页信息
    a. 获取我的id
    b. 获取我的关注
    c. 获取他们最近的推文
3. 白名单
    a. 找推文
    b. 判断
    c. 关注，点赞，转推

setup steps:
1. create developer account at https://developer.twitter.com/en (I'm using the API V2 here, coz V1 is not accessible)
2. go to the developer portal, then go to the User authentication settings, then make OAuth 1.0a on and click it "Read and write", put CallbakcURL "https://127.0.0.1" (local host, we don't use that, so doesn't matter)
3. go back to the developer portal, click the "Keys and tokens", generate "Access Token and Serect"
4. create a .env file, put your API_KEY, API_KEY_SECRET, ACCESS_TOKEN and ACCESS_TOKEN_SECRET
5. you are ready to go !!!

how does the scipt work ?
1. connect to twitter api server using Tweepy package 
2. get all acounts that I followed 
3. find their recent tweets
4. for every tweet, if at least one of the keywords list ("giveaway" ....) in the tweet, we consider it as giveway tweet. So we acts:
    a. follow all twitter accounts metionned 
    b. like the tweet
    c. retweet 
    d. reply/tag  

userful urls:
- https://docs.tweepy.org/en/stable/client.html
- https://github.com/tweepy/tweepy/tree/master/examples/API_v2