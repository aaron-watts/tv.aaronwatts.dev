# No-Cost TV Show Episode Updates Over RSS

[https://tv.aaronwatts.dev](https://tv.aaronwats.dev)

### Step 1: Clone the repo

`git clone https://github.com/aaron-watts/tv.aaronwatts.dev.git`

### Step 2: Delete my shows

Delete my shows from `src/shows.py`, unless you like them, of course!

### Step 3: Push the Repo

Push to your github.

### Step 4: Set up Github Pages

Set up a Project Github Pages for your repo. You will need set Github Pages to deploy from `branch:main` and set `/docs` as the root folder.

### Step 5: Add your shows

You can easily find the ID's for the shows you want to follow using the web page that is now at your project's Github Pages site. This is normally `<username>.github.io/<repository-name>`, unless you have configured your own DNS. You only need to add the ID's in string format to the Python dict, I also put the shows name in as a comment so I can easily see what I've already put in the dict.

### Step 6: Subscribe to your feed!

Unless you have configured your own DNS, this will be at `<username>.github.io/<repository-name>/feed`. You can also copy the link for the RSS logo on your Github Pages website.

## The Website

This project is designed to be no-cost, so the website is static. It is just a tool to easily find the correct ID's for the shows you want to follow, so you can put them in `src/shows.py`, but I got a little carried away.

## Coming Soon: Use your RSS feed to pipe new episodes into a Goggle Calendar!