## Giveaway bot on Twitter with Twitter API V2

setup steps:
1. create developer account at https://developer.twitter.com/en (I'm using the API V2 here, because V1 is not accessible)
2. go to the developer portal, then go to the User authentication settings, then make OAuth 1.0a on and click it "Read and write", put CallbakcURL "https://127.0.0.1" (local host, we don't use that, so doesn't matter)
3. go back to the developer portal, click the "Keys and tokens", generate "Access Token and Serect"
4. create a .env file, put your API_KEY, API_KEY_SECRET, ACCESS_TOKEN and ACCESS_TOKEN_SECRET
5. run "pip install -r requirements.txt"
6. you are ready to go !!!

how does the scipt work ?
1. connect to twitter api server using Tweepy package 
2. get all acounts that I followed 
3. find their recent tweets
4. for every tweet, if at least one of the keywords list ("giveaway" ....) in the tweet, we consider it as giveway tweet. So we acts:
    - follow all twitter accounts metionned 
    - like the tweet
    - retweet 
    - reply/tag  

!!! don't give up when you don't get the expansions with API V2 client. becasue the print function would only the original strings.
we can access the user's follower by `xx["data"]["public_metrics"][followers_count]`
Explanation here:  https://stackoverflow.com/questions/70371657/problem-with-getting-tweet-fields-from-twitter-api-2-0-using-tweepy


userful urls:
- https://docs.tweepy.org/en/stable/client.html
- https://github.com/tweepy/tweepy/tree/master/examples/API_v2
- https://docs.tweepy.org/en/v4.4.0/faq.html#why-am-i-not-getting-expansions-or-includes-data-with-api-v2-using-client

