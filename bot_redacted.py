# bot.py
from twitchio.ext import commands
import time
import tweepy

auth = tweepy.OAuthHandler('***********', '*************')
auth.set_access_token('***********', '************')
api = tweepy.API(auth)

last_tweet = {}

bot = commands.Bot(
    # set up the bot
    irc_token='*********',
    client_id='*********',
    nick='AmanyBelay',
    prefix='$',
    initial_channels=['#AmanyBelay']
)


@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"tweetbot is online!")


@bot.command(name='tweet')
async def tweet(ctx):
	print('hi')
	tweet_content = (str(ctx.content[7:]).replace(r'\n','\n'))

	if not (ctx.author.is_subscriber):
		await ctx.channel.send("@"+ctx.author.name+" is not a subscriber, cannot tweet")

	else:
		if len(tweet_content) > 280:
			await ctx.channel.send("hey @"+ctx.author.name+", your tweet was too long. Shorten it up!")

		else:
			try:
				if (time.time() < last_tweet[ctx.author.name] + 21600):
					await ctx.channel.send("slow down @"+ctx.author.name+", you gotta wait 6 hours between tweets")
				else:
					tweet = api.update_status(tweet_content)
					api.update_status('@amany_belay this tweet was written by Twitch user @'+ctx.author.name+'! If this is my most popular tweet of the week, they will win $25! Like and retweet to help them win!\n(if the above tweet is harmful/violent please dm me and I can take it down)', in_reply_to_status_id = tweet.id)
					#twitter api send
					last_tweet[ctx.author.name] = time.time()
					await ctx.channel.send("@"+ctx.author.name+" tweeted: " + ctx.content[7:])
					await ctx.channel.send("check out the tweet here: https://twitter.com/amany_belay/status/"+str(tweet.id))


			except:
				tweet = api.update_status(tweet_content)
				api.update_status('@amany_belay this tweet was written by Twitch user @'+ctx.author.name+'! If this is my most popular tweet of the week, they will win $25! Like and retweet to help them win!\n(if the above tweet is harmful/violent please dm me and I can take it down)', in_reply_to_status_id = tweet.id)
				#twitter api command(tweet_content)
				last_tweet[ctx.author.name] = time.time()
				await ctx.channel.send("@"+ctx.author.name+" tweeted: " + ctx.content[7:])
				await ctx.channel.send("check out the tweet here: https://twitter.com/amany_belay/status/"+str(tweet.id))


if __name__ == "__main__":
    bot.run()