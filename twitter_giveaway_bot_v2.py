from dotenv import dotenv_values
import tweepy, re, time, random

# condition keywords for giveaway tweets
lst_keywords = ["giveaway", "give away", "giving away", "participate", "participating"]


def connect():
    """connect to twitter api

    Returns:
        _type_: Tweepy client
    """
    # global config
    config = dotenv_values(".env")

    # create your client
    client = tweepy.Client(
        bearer_token=config["BEARER_TOKEN"],
        consumer_key=config["API_KEY"],
        consumer_secret=config["API_KEY_SECRET"],
        access_token=config["ACCESS_TOKEN"],
        access_token_secret=config["ACCESS_TOKEN_SECRET"],
    )

    return client


def get_accounts_following(client):
    """_summary_

    Args:
        client (_type_): Tweepy client
    """
    # get my twitter id
    my_info = client.get_me().data
    my_id = my_info["id"]
    print(f"-" * 80)
    print(f"my_info: {my_info}")
    print(f"my_id: {my_id}")

    # get all accounts that I am following
    users_following = client.get_users_following(my_id, user_auth=True).data
    users_name = [user["name"] for user in users_following]
    # users_id = [user["id"] for user in users_following]
    print(f"users_following {users_name}")

    return users_following


def get_accounts_followers(client):
    """_summary_

    Args:
        client (_type_): Tweepy client
    """
    # get my twitter id
    my_info = client.get_me().data
    my_id = my_info["id"]
    print(f"-" * 80)
    print(f"my_info: {my_info}")
    print(f"my_id: {my_id}")

    # get all accounts that follow me
    users_followers = client.get_users_followers(my_id, user_auth=True).data
    users_name = [user["name"] for user in users_followers]
    print(f"users_followers {users_name}")

    return users_followers


def finsh_task(client, user, name_users_followers, max_results=10):
    """
    Finsh the GIVEAWAY task for one user

    Args:
        client (_type_): Tweepy client
        user (tweepy.user.User):  twitter users that I followed with id and name
        name_users_followers (list):  list of twitter users' username that follow me
        max_results (int): max tweet for one user
    """

    # latest_tweets = client.get_users_tweets(
    #     user["id"],
    #     user_auth=True,
    #     max_results=max_results,
    #     tweet_fields=["text"],
    #     expansions=["referenced_tweets.id"],
    # ).data

    latest_tweets = client.get_users_tweets(
        user["id"],
        user_auth=True,
        max_results=max_results,
        tweet_fields=["text"],
        expansions=["referenced_tweets.id"],
    ).includes["tweets"]

    for one_tweet in latest_tweets:
        tweet_id = one_tweet["id"]
        content = one_tweet["text"]

        # check whitelist condition
        count_keywords = sum(
            [1 if keyword in content.lower() else 0 for keyword in lst_keywords]
        )
        if count_keywords > 1:
            print("-" * 80)
            print(content)
            # check participation criteria
            # 1. follow
            # find all users begining with @
            users_need_to_follow = set(re.findall(r"@([a-zA-Z0-9_]+)", content))

            for user_name in users_need_to_follow:
                # get user id
                user_id = client.get_user(username=user_name, user_auth=True).data.id
                # follow
                res = client.follow_user(user_id).data["following"]

                print(f"user_name: {user_name}")
                print(f"user_id: {user_id}")
                print(f"following: {res}")

            # 2. like
            res = client.like(tweet_id).data["liked"]
            print(f"liked: {res}")

            # 3. retweet
            res = client.retweet(tweet_id).data["retweeted"]
            print(f"retweeted: {res}")

            # # 4. tag
            # tag_message = (
            #     "".join(["@" + user for user in users_need_to_follow])
            #     + "Thank you very much!"
            # )
            # res = client.create_tweet(text=tag_message, in_reply_to_tweet_id=tweet_id)

            # 5. tag friends
            # msg => 1. tag up to 3 friends (every tag is an extra entry)
            #        2. Tag 3 NFT frens

            tag_message = re.findall(r"tag.+fr", content.lower())
            if len(tag_message) > 0:
                # find if need to tage friends
                try:
                    n_friends = int(re.findall(r"[0-9]", tag_message[0])[0])
                except:
                    print("dont find the number of friends")
                    print(f"tag message: {tag_message}")
                    n_friends = 3

                # choose friends
                selected_friends = random.sample(name_users_followers, n_friends)

                # set message
                tag_message = "".join(["@" + user for user in selected_friends])
                res = client.create_tweet(
                    text=tag_message, in_reply_to_tweet_id=tweet_id
                )

            # wait
            time.sleep(1)


def main():
    client = connect()
    users_following = get_accounts_following(client)
    users_followers = get_accounts_followers(client)
    name_users_followers = [i["username"] for i in users_followers]
    for user in users_following[:20]:
        print("-" * 80)
        print(user)
        finsh_task(client, user, name_users_followers)


if __name__ == "__main__":
    main()
