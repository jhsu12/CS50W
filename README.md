
CS50W Project1 Wiki
===


## General info
Design a Wikipedia-like online encyclopedia.



## Specification
- **Entry Page**<br/>
Visiting `/wiki/TITLE`, where `TITLE` is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.
- **Index Page**<br/>
Update `index.html` such that, instead of merely listing the names of all pages in the encyclopedia, user can click on any entry name to be taken directly to that entry page.
- **Search**<br/>
Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry.
- **New Page**<br/>
Clicking “Create New Page” in the sidebar should take the user to a page where they can create a new encyclopedia entry.
- **Edit Page**<br/>
On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a `textarea`.
- **Random Page**<br/>
Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.

- **Markdown to HTML Conversion**<br/>
On each entry’s page, any Markdown content in the entry file should be converted to HTML before being displayed to the user. You may use the `python-markdown2` package to perform this conversion, installable via `pip3 install markdown2`.
## Technologies

- Python Django
- HTML
- CSS


## Demo
[![Click here for the demo video](https://img.youtube.com/vi/adTorGWRqPw/0.jpg)](https://youtu.be/adTorGWRqPw)
