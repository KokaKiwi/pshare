P'Share
=======

A small private pad where you can receive messages fully privately.

P'Share allow you to create a private pad where others users can post messages which only you can read.

Demo: [https://p.kokakiwi.net](https://p.kokakiwi.net)

Installation
------------

First, create your web environment.

```sh
    virtualenv --no-sites-package env
    cd env
    source bin/activate
```

Install pshare dependencies

```sh
    pip install flask sqlalchemy
```

Clone pshare repository

```sh
    git clone https://github.com/KokaKiwi/pshare.git
    cd pshare
```

And start your server!

```sh
    python ./pshare.py
```

Usage
-----

### Quick pad creation
Press 'enter' key two times on home page in order to generate your pad ID and password, and to go to your pad page.

### Custom pad creation
Enter your pad ID (ex: 'toto') and your pad password (ex: 'toto') to create an unique pad you can retrieve later by entering same ID/password.

### Pad usage
Just send the public pad URL to others users to let them send messages to you.

Currently, you must refresh you pad page in order to retrieve sent messages.

Some screenshots
----------------

![home page](http://i.imgur.com/dVyIybZ.png "Home page")

![pad page](http://i.imgur.com/KisTBN9.png "Pad page")
