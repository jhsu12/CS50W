document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox', false));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent', false));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive', false));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function send_email(event) {
  event.preventDefault();
  
  // Get the value of recipients, subject and body
  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;
  

  // POST
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: `${body}\n`
    })
  })
  .then(response => response.json())
  .then(result => {

    // Error exists
    if(result.error !== undefined)
    {
      
      document.querySelector('#error').innerHTML = `
        <div class="alert alert-danger" role="alert">
          ${result.error}
        </div>`;
      compose_email;
      
    }
    // Email sent successfully
    else
    {
      document.querySelector('#message-text').innerHTML = 'Email sent successfully.';
      load_mailbox('sent', true);
    }
    
    
  })
  
  
  
  
  
  
}

function compose_email() {
  
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-email').style.display = 'none';

  // Clear error
  document.querySelector('#error').innerHTML ='';
  

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function archive_button(email_id, archived)
{
  // Update archived
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !archived
    })
  })
  .then(() => {
    
    if(archived)
    {
      document.querySelector('#message-text').innerHTML = 'Email unarchived successfully!';
      //console.log("1");
    }
    else
    {
      document.querySelector('#message-text').innerHTML = 'Email archived successfully.';
      //console.log("2");
    }
    
  })
  // Get back to inbox
  .then(() => load_mailbox('inbox', true));
  
  
  
} 

function reply_button(email_id)
{
  // Show compose_email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-email').style.display = 'none';
  document.querySelector('#message').style.display = 'none';

  // Clear error
  document.querySelector('#error').innerHTML ='';

  
  // GET email
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    // Re: subject when first reply
    let subject = email.subject;
    if(!subject.startsWith('Re: '))
    {
      subject = `Re: ${subject}`;
    }

    // Pre-fill form 
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value = subject;
    document.querySelector('#compose-body').value = `\nOn ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
      
  
    
  });
}

function view_email(email_id, mailbox) {

  // Show view_email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'block';
  document.querySelector('#message').style.display = 'none';
  

  
  // GET email
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      // ... do something else with email ...
      let sender = email.sender;
      let recipients = email.recipients;
      let subject = email.subject;
      let body = email.body;
      let timestamp = email.timestamp;
      let archived = email.archived;
      let ar_text = 'Archive';

      body = body.replace(/\n/g, '<br />');
      console.log(body);

      if(archived)
      {
        ar_text = 'Unarchive';
      }
      
      //console.log(email);
     

      // Update innerhtml
      const element = document.querySelector('#view-email');

      // No reply and archive button in sent mails
      if(mailbox === 'sent')
      {
        element.innerHTML = `
        <br>
          <p><b>From: </b> ${sender}</p>
          <p><b>To: </b> ${recipients}</p>
          <p><b>Subject: </b> ${subject}</p>
          <p><b>Timestamp: </b> ${timestamp}</p>
        <br>
         
        <hr>
        <br>
        <p>${body}</p>`;
      }
      else
      {
        element.innerHTML = `
        <br>
          <p><b>From: </b> ${sender}</p>
          <p><b>To: </b> ${recipients}</p>
          <p><b>Subject: </b> ${subject}</p>
          <p><b>Timestamp: </b> ${timestamp}</p>
        <br>
          <button type="button" class="btn btn-primary" id="reply-button">Reply</button>
          &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
          <button type="button" class="btn btn-warning" id="archive-button">${ar_text}</button>
        <hr>
        <br>
        <p>${body}</p>`;

        // Archive or Unarchive
        document.querySelector('#archive-button').addEventListener('click', () => archive_button(email_id, archived));

        // Reply 
        document.querySelector('#reply-button').addEventListener('click', () => reply_button(email_id));
      
      }

      

      // Mark as read
      if(!email.read)
      { 
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        });
      }

      

    
            
    });
}
function load_mailbox(mailbox, message) {

  // GET request to mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);

    // ... do something else with emails ...
    emails.forEach(email => {

      // get the required value
      let sender = email.sender;
      let subject = email.subject;
      let timestamp = email.timestamp;
      let read = email.read;

      //create html
      const element = document.createElement('div');
      element.className = "container";
      element.style.border = '1px solid black';
      if(read)
      {
        element.style.backgroundColor = 'LightGray';
      }
      
      

      element.innerHTML = ` 
        <span class="sender col-3"> <b>${sender}</b> </span>
        <span class="subject col-6"> ${subject} </span>
        <div style="margin-left: 900px; position: relative;">
        <span class="text-muted"> ${timestamp} </span>
        </div>
        
        `;

      
      element.addEventListener('click', () => view_email(email.id, mailbox));
      document.querySelector('#emails-view').append(element);
    });
  })
  .then(() => {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#view-email').style.display = 'none';
    
    // if sent successfully, show message
    if(message)
    {
      document.querySelector('#message').style.display = 'block';
    }
    else
    {
      document.querySelector('#message').style.display = 'none';
    }
  });
  
  

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  
}