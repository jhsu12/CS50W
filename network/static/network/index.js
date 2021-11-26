document.addEventListener("DOMContentLoaded", function() {
    console.log("DOMContentLoaded");


    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            console.log(button.dataset.action);

            if(button.dataset.action == 'edit')
            {
                edit(button);
            }
            
            else if(button.dataset.action == 'like' || button.dataset.action == 'unlike')
            {
                like_button(button);
            }
            
            
        };
    });
   
});

function like_button(button)
{
    
    console.log('in like');
    post_id = button.dataset.postid;
    action = button.dataset.action;
    like_count = document.querySelector(`#like_${post_id}`).querySelector('#count').querySelector("p");

    if(action == "like")
    {
        console.log("IN like");
        // PUT request to add request.user to liked_post
        fetch(`/posts/${post_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                action: "like",
                liked: true, 
            })
        });

        // Change the innerHTML of like_button 
        //document.querySelector(`#like_${post_id}`).querySelector('#button').innerHTML = '<button onclick="like_button(this)" data-action="unlike" data-postid= "{{ post.id }}" type="button" class="btn btn-primary btn-sm">Like</button>';
        /*
        document.querySelector(`#like_${post_id}`).querySelector('#button').setAttribute("class", "btn btn-primary btn-sm");
        document.querySelector(`#like_${post_id}`).querySelector('#button').setAttribute("data-action", "unlike");
        document.querySelector(`#like_${post_id}`).querySelector('#button').setAttribute("onclick", "like_button(this)");
        */
        document.querySelector(`#like_${post_id}`).querySelector('#like').style.display = 'block';
        document.querySelector(`#like_${post_id}`).querySelector('#unlike').style.display = 'none';
        // Like count +1
        like_count.innerHTML = parseInt(like_count.innerHTML) + 1;

        // Show like count
        like_count.style.display = "block";
    }
    else if(action == "unlike")
    {
        console.log("IN unlike");
        // PUT request to remove request.user to liked_post
        fetch(`/posts/${post_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                action: "like",
                liked: false, 
            })
        });

        // Change the innerHTML of like_button 
        //document.querySelector(`#like_${post_id}`).querySelector('#button').innerHTML = '<button onclick="like_button(this)" data-action="like" data-postid= "{{ post.id }}" type="button" class="btn btn-light btn-sm">Like</button>';
        
        /*document.querySelector(`#like_${post_id}`).querySelector('#button').setAttribute("class", "btn btn-light btn-sm");
        document.querySelector(`#like_${post_id}`).querySelector('#button').setAttribute("data-action", "like");
        document.querySelector(`#like_${post_id}`).querySelector('#button').setAttribute("onclick", "like_button(this)");*/

        document.querySelector(`#like_${post_id}`).querySelector('#unlike').style.display = 'block';
        document.querySelector(`#like_${post_id}`).querySelector('#like').style.display = 'none';
        // Like count -1
        like_count.innerHTML = parseInt(like_count.innerHTML) - 1;

        // If like count == 0, hide like_count
        if(parseInt(like_count.innerHTML) == 0)
        {
            like_count.style.display = "none";
        }

    }
}
function save(post_id, new_content)
{   
    
    // Put request to update the database
    //new_content = document.querySelector(`#edit_form_${post_id}`).querySelector('textarea').innerHTML;
    console.log('save');
    fetch(`/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            action: "save",
            content: new_content,
        })
    })

    // Update id="content_{{ post.id }}".innerHTML to the latest content
    document.querySelector(`#content_${post_id}`).innerHTML = new_content;


    // Show post content, Hide edit form and Change edit button's innerHTML
    document.querySelector(`#content_${post_id}`).style.display = 'block';
    document.querySelector(`#edit_form_${post_id}`).style.display = 'none';
    document.querySelector(`#edit_${post_id}`).innerHTML = 'Edit';
    document.querySelector(`#like_${post_id}`).style.display = 'block';
    
}
function cancel(post_id)
{
    console.log('cancel');
    // Show post content, Hide edit form and Change edit button's innerHTML
    document.querySelector(`#content_${post_id}`).style.display = 'block';
    document.querySelector(`#edit_form_${post_id}`).style.display = 'none';
    document.querySelector(`#edit_${post_id}`).innerHTML = 'Edit';
    document.querySelector(`#like_${post_id}`).style.display = 'block';
}
function edit(button)
{

    post_id = button.dataset.postid;
    edit_form = document.querySelector(`#edit_form_${ post_id }`);
    text_area = edit_form.querySelector('textarea');

    // Hide post content, Show edit form and Change edit button's innerHTML

    document.querySelector(`#content_${post_id}`).style.display = 'none';
    document.querySelector(`#like_${post_id}`).style.display = 'none';
    edit_form.style.display = 'block';
    document.querySelector(`#edit_${post_id}`).innerHTML = '';

    // Autofill original post content to form
    
    fetch(`/posts/${post_id}`)
    .then(response => response.json())
    .then(post => {
        console.log(`original: ${post.content}`);
        autofill = post.content;
        text_area = edit_form.querySelector('textarea');
        text_area.value = autofill;
    });
    //autofill = document.querySelector(`#content_${post_id}`).innerHTML;
    
    new_content = '';

    text_area.addEventListener('change', function(ele) {
        new_content = ele.target.value;
        console.log(new_content);
    });

    // When Save or Cancel is clicked
    edit_form.querySelectorAll('button').forEach(but => {

        but.onclick = function()
        {
            if(but.dataset.action == 'save')
            {
                save(post_id, new_content)
            }
            else
            {
                cancel(post_id)
            }
        };
    });
        
        
    
    
}




