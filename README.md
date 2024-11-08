# secret-santa-function
A serverless, databaseless, url-based implementation of secret santa

This version uses google app engine as I had some stability problems with azure functions

To start, hit the function url with no params, you'll get a basic UI to enter a list of names on.
Hit enter and you'll redirect and get a list of names with links for each person that includes their target baked in to the URL.
Now you can send those links to whoever you want and they just need to click it.
The UI for the clicked link is slightly higher effort to make it easy for even older people to understand.

Generate requirements.txt
`poetry export --without-hashes --format=requirements.txt > requirements.txt`