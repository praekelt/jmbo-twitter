Changelog
=========

0.4.1
-----
#. Up minimum required `jmbo` to 1.1.1.
#. Set a timeout of 10 seconds to prevent stuck tasks.

0.4
---
#. New content type `Search` allows tweets to be retrieved by term or hashtag.

0.3.2
-----
#. Increase cache time so we can survive Twitter outages better.

0.3.1
-----
#. Protect against cache destruction if Twitter throttles us.

0.3
---
#. Fetch updates asynchronously.

0.2.2
-----
#. Cache templates.

0.2.1
-----
#. Actually respect the force parameter when fetching tweets.
#. Clean up confusing code.

0.2
---
#. Handle Twitter's new API v1 which requires authentication.

0.1.4.1
-------
#. More defensive code in the event of python-twitter breaking.

0.1.4
-----
#. Do not use slug as the Twitter identifier anymore since it may clash.

0.1.3
-----
#. Make admin resilient in case admin_urls.py is not in settings.

0.1.2
-----
#. Fix bug where the twitter account name may be overridden.

0.1.1
-----
#. Fix serious bug where new feeds could not be added.

0.1
---
#. First release.

