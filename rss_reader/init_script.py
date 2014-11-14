from main.models import *

lemon = User.objects.create_user('lemon')

comics = Topic(name='Comics', user=User.objects.all()[0])
comics.save()

xkcd = Feed.createByURL('http://xkcd.com/rss.xml')
comics.feeds.add(xkcd)
comics.save()

ques_content = Feed.createByURL('http://www.questionablecontent.net/QCRSS.xml')
comics.feeds.add(ques_content)
comics.save()

broodhollow = Feed.createByURL('http://broodhollow.chainsawsuit.com/feed/')
comics.feeds.add(broodhollow)
comics.save()

escapist = Feed.createByURL('http://rss.escapistmagazine.com/videos/list/1.xml')
comics.feeds.add(escapist)
comics.save()


science = Topic(name='Science', user=User.objects.all()[0])
science.save()

nytimes = Feed.createByURL('http://rss.nytimes.com/services/xml/rss/nyt/Science.xml')
science.feeds.add(nytimes)
science.save()

feedburner = Feed.createByURL('http://feeds.feedburner.com/kernelmag?format=xml')
science.feeds.add(feedburner)
science.save()

taxonomy = Feed.createByURL('http://www.popsci.com/taxonomy/term/100136/feed')
science.feeds.add(taxonomy)
science.save()

exit