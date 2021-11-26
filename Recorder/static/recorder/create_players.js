document.addEventListener('DOMContentLoaded', function() {
    console.log("in");
    //clear successfully_created list
    clear_successfully_created_list;
    document.querySelector('#create_button').addEventListener('click', create_player);
});

function create_player(event)
{
    event.preventDefault();
    console.log("create");

    // Get the data
    const name = document.querySelector('#inputName').value;
    const number = document.querySelector('#inputNumber').value;
    const image = document.querySelector('#inputImageURL').value;

    //position
    const g = document.querySelector('#G');
    const c = document.querySelector('#C');
    const f = document.querySelector('#F');

    let position = "";

    if(g.checked)
    {
        position = g.value;
    }
    else if(c.checked)
    {
        position = c.value;
    }
    else
    {
        position = f.value;
    }

    console.log(name);
    // Send the data back to API
    
    fetch("/create", {
        method: 'PUT',
        body: JSON.stringify({
            name: name,
            number: number,
            image: image,
            position: position,
        })
    })
    .then(response => response.json()) //Something wrong right here!
    .then(result => {

        //console.log(result.test);
        
        message = document.querySelector('#message');
        //error exists
        if(result.error !== undefined)
        {
            //Show error alert
            message.innerHTML = `<div class=" alert alert-danger" role="alert"> ${result.error} </div>`;
            message.style.display = 'block';
        }
        //Successfully created player
        else
        {
            //Show successful alert
            message.innerHTML = `<div class=" alert alert-success" role="alert">${result.successful} </div>`;
            message.style.display = 'block';
            
            //Append player to successfully created list

            new_list = document.createElement("li");
            new_list.innerText = `#${result.number} ${result.name}`;
            document.querySelector('#list').appendChild(new_list);

            //Show successfully created list
            document.querySelector('#successfully_created').style.display = 'inline-block';
            
            //Clear the form
            document.querySelector("form").reset();
            
        }
        
    })
   
    
}

function clear_successfully_created_list()
{
    let element = document.getElementById("list");
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}