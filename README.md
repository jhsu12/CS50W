
CS50W Project2 Commerce
===


## General info

Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

## Technologies

- Python Django
- HTML
- CSS

## Specification

- **Models**<br/>
Your application should have at least three models in addition to the `User` model: one for auction listings, one for bids, and one for comments made on auction listings. It’s up to you to decide what fields each model should have, and what the types of those fields should be. You may have additional models if you would like.

- **Create Listing**<br/>
Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).

- **Active Listings Page**<br/>
The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page should display (at minimum) the title, description, current price, and photo (if one exists for the listing).

- **Listing Page**<br/>
Clicking on a listing should take users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.

- **Watchlist**<br/>
Users who are signed in should be able to visit a Watchlist page, which should display all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.

- **Categories**<br/>
Users should be able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.

- **Django Admin Interface**<br/>
Via the Django admin interface, a site administrator should be able to view, add, edit, and delete any listings, comments, and bids made on the site.




## Demo
[![Click here for the demo video](https://img.youtube.com/vi/KrC_B9VHjdg/0.jpg)](https://youtu.be/KrC_B9VHjdg)
