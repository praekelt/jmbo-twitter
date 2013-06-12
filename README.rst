Jmbo Twitter
============
**Jmbo app to fetch and display tweets as listings.**

.. contents:: Contents
    :depth: 5

Installation
------------

#. Install or add ``jmbo-twitter`` to your Python path.

#. Add ``jmbo_twitter`` to your ``INSTALLED_APPS`` setting.

Usage
-----

Twitter's API version 1 requires authentication. Obtain authentication info at https://dev.twitter.com/apps.
The following setting is required::
    
    JMBO_TWITTER = {
        'consumer_key': 'XXX', 
        'consumer_secret': 'XXX', 
        'access_token_key': 'XXX', 
        'access_token_secret': 'XXX'
    }

