# Stateless secret santa
A stateless, databaseless, url-based implementation of secret santa

**Now deployed at [santa.nics.work](https://santa.nics.work)**
> The price limit is hard-coded to $50 right now (I really just use this for my family so I just change it when needed)

This version uses google app engine as I had some stability problems with azure functions (most likely due to cold starting). Azure functions version is still available at branch [release/azure-functions](nvonahsen/secret-santa-function/tree/release/azure-functions) though I may forget to update it at some point.

To start, hit '/' or '/create'
Use to UI to enter a list of names and generate links for each person that includes their target baked in to the URL.
Now you can send those links to whoever you want and they just need to click it.

## Future
I make a few upgrades to this app every now and again when a holiday comes around, so will probably fix the price limit next time. I wanna allow numbers in the seed as well, but still keep the URLs short, so I'll do some investigating on optimising the encoding, maybe something based on UTF to allow 3-bit common letters? I might also give up and just make the app start writing things to disk, though that means I need to start thinking about security and stuff which is a pain...

## Deploying your own
(if you're new to google cloud)
- Create a google cloud platform (GCP) account (free trial is fine)
- In the google cloud console create a project (I think it actually auto-creates your first one) - *The project name will appear in your default URL, so if you want it to read nicely maybe make a project with a good name*
- Install the `gcloud` command line interface https://cloud.google.com/sdk/docs/install
- `gcloud auth login` in your terminal to sign in to your google cloud environment
- `gcloud app deploy` in the root directory of this project (where app.yaml is) to deploy the application ***<-** This is the only bit that isn't just google cloud setup, if you know what you're doing somewhat you should be able to just run this (making sure your CLI is pointing to the correct google cloud project if you already have some `gcloud config set project <your-project-id>`)*

Google app engine will provide you with a url like `your-project-name.ts.r.appspot.com` this will work fine, and have https.
If you want your own domain, that's gonna be a you problem, but it's easy to set up with gcp.

## Dev
I use poetry, it's neat, manages packages nicely for your project and stuff. You can find info about it and install instructions at [python-poetry.org](https://python-poetry.org/)

If you change the requirements you'll need to generate requirements.txt *(GCP uses this to know what packages to install, since it doesn't support poetry)*
`poetry export --without-hashes --format=requirements.txt > requirements.txt`

`start-windows.ps1` should allow you to run the app locally on a windows pc which I happend to dev this on. If you're running on linux/mac you should be able to `poetry run flask --app main run` since flask can run itself on these operating systems (windows need an extra layer to actually run it, in this case "waitress")

