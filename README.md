# FILAB Canopus
## Introduction
This project aims to be a simple way to change a password for FIWARE Lab users. There was no 
other way to do this except asking for a password change to the Node adminitrators.

When an user requests a password, an email will be sent to the user with a code. Once clicked in the code, a new password will be generated and the user will be able to access FIWARE Lab (https://cloud.lab.fiware.org) with their new password.

It is **highly recommended** to change the password as soon as possible y the cloud portal.

## User Manual
Basically, you can POST to the address where it is installed asking for a password change:
 curl -X POST <url>/filab-passwrods/reset/somebody@example.com

This will send you an email with a link to confirm the password. By clicking in the link, it
will change the password with a random one, and will send another email confiming the password
change.

These are the specifications:

### POST /reset/<string:mail>

This one requests an url which will be sent by email to the email given as parameter.

     curl -X POST https://cloud.lab.fiware.org/filab-passwords/reset/somebody@example.com
     "A confirmation message has been sent to your email"

The expected return value is **HTTP/200**. The link will expire 24 hours after the mail is sent.
If 2 requests are submitted, the second one will invalidate the first one.


### GET /confirm/<string:code>
You will get by email a link which will confirm a password change to the user. The kind of 
link is something like this:

     curl https://cloud.lab.fiware.org/filab-passwords/confirm/TPL9z5WwTI8zn7cxS5qcKK269V2JgTzr6tpCwZt9xMWSIFzrv9jMTvDMfooAvEM13r2uFK3b9ouNwCxMDkrUJpX5TkWyjhgINKDc9oThq3SM6usyCdlj3r2aGB7uUNy0

When you click the link, you can have 

* *HTTP/404 - Not found* if the code is not valid (it never was valid or it has expired)
* *HTTP/200 - OK* if the code is valid, and the password for the user will be changed.

### Installation
In order to install the service, it should be cloned from Github and the requirements should
be installed in their own virtualenv.

    $ https://github.com/jicarretero/FILAB-Canopus
    ...
    $ cd FILAB-Canopus
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

Once done this, we should edit ``config.ini`` file to configure things:
    [keystone]
    # User who can do a password change. This is usually an admin user. And its password
    user=admin
    password=whateverpassword
    
    # Keystone auth URL. 
    url=http://cloud.lab.fiware.org:4730
    
    [server]
    # Where the service is installed. The service base URL
    base_url=https://cloud.lab.fiware.org/filab-passwords
    
    [email]
    # This is the email SMTP server used to send mails to the users
    host=host.youremailserver.com

    # The from of the email.
    from=whoever@host.youremailserver.com
    
    # The from shown in the email clients.
    from_name=whoever <whoever@host.youremailserver.com>
    
    # These are the files used to email the user that a password change request has been issued
    # Under "Resources" there are the examples
    recover_html_template=Resources/recover_text_template.html
    recover_text_template=Resources/recover_text_template.txt
    
    # The subject of the email sent when a recover password has been issued.
    recover_subject=The Subject to be sent in your recover file
    
    # These are the files used to email the user the password change is effective
    # Under "Resources" there are the examples
    new_password_html_template=Resources/new_password_text_template.html
    new_password_text_template=Resources/new_password_text_template.txt
    
    # The subject of the email sent when a recover password has been issued.
    new_password_subject=The Subject for the new password
    
    [memcached]
    # This is quite useful. Should be used. Just simple configuration parameters.
    use_memcached=True
    memcached_host=localhost
    memcached_port=11211

Now, every time we want to start (locally) the server, we can:

    $ source venv/bin/activate
    $ python main.py

There's one file we could consider editing when we try to make this run under Apache. The
file is ``filab-password.wsgi``. This line should be changed in order to make things work
whith the virtual environment we should have created.

    # Change this line in order to meet your virtualenv.
    activate_this = base_path + '/venv/bin/activate_this.py'

