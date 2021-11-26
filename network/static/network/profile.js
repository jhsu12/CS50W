document.addEventListener("DOMContentLoaded", function() {
    document.querySelector('#follow_button').addEventListener('click', follow);
});

function follow()
{
    // Get the value
    button = document.querySelector('#follow_button');
    text = button.innerHTML;
    visit = button.dataset.profile;
    action = "delete"

    if(text == "Follow")
    {
        action = "create"
    }

    // Post
    fetch('/follow_button', {
        method: 'POST',
        body: JSON.stringify({
            visit: visit,
            action: action,
            
        })
      })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        // Update followers
        fetch(`/follow_button/${visit}`)
        .then(response => response.json())
        .then(result => {
            // Print emails
            console.log(result);
            document.querySelector('#followers').innerHTML = result.followers;
            // ... do something else with emails ...
        });
          
    });
    // Update button.innerhtml
    if(text == "Follow")
    {
        button.innerHTML = "Unfollow";
    }
    else
    {
        button.innerHTML = "Follow";
    }

    
}