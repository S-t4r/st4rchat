document.addEventListener('DOMContentLoaded', () => {

    // ### Edit
    document.querySelectorAll('.edit_button').forEach(button => {
        button.addEventListener('click', () => {

            const post_id = button.getAttribute('data_post_id');
            
            // Add your event handling logic here
            
            // If edit button is first clicked.
            if (button.innerText === 'Edit') {
                const post_content_element = document.getElementById(`post_content_${post_id}`);
                post_element = post_content_element;

                const post_content = post_content_element.innerText;
    
                let textarea = document.createElement('textarea');
                textarea.value = post_content;
                textarea.id = `textarea_${post_id}`;
                
                let cancel_button = document.createElement('button');
                cancel_button.className = 'btn btn-warning mx-2'
                cancel_button.innerText = 'Cancel';
                cancel_button.addEventListener('click', () => {

                    textarea.replaceWith(post_content_element);
                    cancel_button.remove();
                    button.innerText = 'Edit';
                });

                post_content_element.replaceWith(textarea);
                button.innerText = "Save";
                button.insertAdjacentElement('afterend', cancel_button);
            }
            else {
                const textarea = document.getElementById(`textarea_${post_id}`);
                const updated_content = textarea.value;

                const csrf_token = getCookie('csrftoken');
                
                fetch(`/edit/${post_id}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf_token
                    },
                    body: JSON.stringify({
                        post_id: post_id,
                        content: updated_content
                    })
                })
                .then(response => response.json())
                .then(data => {
                    
                    if (data.success) {
                        
                        let content = document.createElement('p');
                        content.id = `post_content_${post_id}`
                        content.innerText = data.content
                        
                        textarea.replaceWith(content)

                        // Remove cancel button
                        button.nextElementSibling.remove();
                        button.innerHTML = 'Edit';
                    }

                    // Handle error 
                    else {
                        console.error('Error updating post:', data.error);
                    }
                });

            }
        });
    });


    // ### Delete
    document.querySelectorAll('.delete_button').forEach(button => {
        button.addEventListener('click', () => {
            const csrf_token = getCookie('csrftoken');
            const post_id = button.getAttribute('data_post_id');

            fetch(`/delete_post/${post_id}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token
                },
                body: JSON.stringify({
                    post_id: post_id,
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById(post_id).remove();
                }
                // Handle error 
                else {
                    console.error('Error updating post:', data.error);
                }
            });
        })
        
    })
    

    
    // ### Like
    document.querySelectorAll(".like_button").forEach(button => {
        button.addEventListener('click', () => {
            handle_like(button);
        })
    })


})




function handle_like(button) {
    const post_id = button.getAttribute('data_post_id');
    
    fetch(`/likes`, {
        method:"POST",
        headers: {
            "Content-type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ post_id: post_id })
    })
    .then(response => response .json())
    .then(data => {
        if (data.success) {
            
            const like_count_element = document.querySelector(`#like_count_${post_id}`);
            like_count_element.innerText = data.new_like_count
        }
    })
}










// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}