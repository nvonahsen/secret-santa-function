# Stateless secret santa
A stateless, databaseless, url-based implementation of secret santa

It uses azure functions because that's what I find easiest to deploy on (plus its free for quite a few calls).

**Now deployed (on google app engine, from main) at [santa.nics.work](https://santa.nics.work)**


This version uses google app engine as I had some stability problems with azure functions (most likely due to cold starting). Azure functions version is still available at branch [release/azure-functions](nvonahsen/secret-santa-function/tree/release/azure-functions) though I may forget to update it at some point.

To start, hit '/' or '/create'
Use to UI to enter a list of names and generate links for each person that includes their target baked in to the URL.
Now you can send those links to whoever you want and they just need to click it.

Generate requirements.txt
`poetry export --without-hashes --format=requirements.txt > requirements.txt`