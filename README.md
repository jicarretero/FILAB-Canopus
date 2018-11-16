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
