# FILAB-ChangePassword
The project is thought to ask for a password to FIWARE Lab in a very simple way.

When an user requests a password, an email will be sent to the user with a code. Once clicked in the code, a new password will be generated and the user will be able to access FIWARE Lab (https://cloud.lab.fiware.org) with their new password.

## POST /reset/<string:mail>

This one requests an url which will be sent by email to the email given as parameter.

     curl -X POST https://cloud.lab.fiware.org/filab-passwords/reset/joseignacio.carretero@fiware.org
     "A confirmation message has been sent to your email"

## GET /confirm/<string:code>

This one will confirm a password change. You can use the link sent by email

     curl https://cloud.lab.fiware.org/filab-passwords/confirm/TPL9z5WwTI8zn7cxS5qcKK269V2JgTzr6tpCwZt9xMWSIFzrv9jMTvDMfooAvEM13r2uFK3b9ouNwCxMDkrUJpX5TkWyjhgINKDc9oThq3SM6usyCdlj3r2aGB7uUNy0
