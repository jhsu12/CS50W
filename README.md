
CS50W Project4 Network
===


## General info

Design a Twitter-like social network website for making posts and following users.

## Technologies

- Python Django
- Javascript
- HTML
- CSS

## Specification

- **New Post**<br/>
Users who are signed in should be able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.

- **All Posts**<br/>
The “All Posts” link in the navigation bar should take the user to a page where they can see all posts from all users, with the most recent posts first.

- **Profile Page**<br/>
Clicking on a username should load that user’s profile page. This page should:
  - Display the number of followers the user has, as well as the number of people that the user follows.
  - Display all of the posts for that user, in reverse chronological order.
  - For any other user who is signed in, this page should also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user should not be able to follow themselves.

- **Following**<br/>
The “Following” link in the navigation bar should take the user to a page where they see all posts made by users that the current user follows.

- **Pagination**<br/>
On any page that displays posts, posts should only be displayed 10 on a page. If there are more than ten posts, a “Next” button should appear to take the user to the next page of posts (which should be older than the current page of posts). If not on the first page, a “Previous” button should appear to take the user to the previous page of posts as well.

- **Edit Post**<br/>
Users should be able to click an “Edit” button or link on any of their own posts to edit that post.

- **“Like” and “Unlike”**<br/>
Users should be able to click a button or link on any post to toggle whether or not they “like” that post.





## Demo
[![Click here for the demo video](https://img.youtube.com/vi/ecKfimlYodw/0.jpg)](https://youtu.be/ecKfimlYodw)
