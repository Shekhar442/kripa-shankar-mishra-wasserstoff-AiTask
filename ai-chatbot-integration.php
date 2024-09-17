<?php
/**
 * Plugin Name: AI Chatbot Integration
 * Description: Integrates an AI chatbot with WordPress
 * Version: 1.0
 * Author: Shekhar Suman
 * Code Explaination: [ The PHP plugin integrates an AI chatbot with WordPress. 
 * It creates an admin settings page for configuring the chatbot's API URL. 
 * It adds a chat interface to the website’s footer. 
 * Users can interact with the chatbot via a text input and send button. 
 * JavaScript sends user messages to the API and displays responses on the site. ]
 **/

// Prevent direct access to this file
if (!defined('ABSPATH')) {
    exit;
}

// Add admin menu
add_action('admin_menu', 'chatbot_admin_menu');

function chatbot_admin_menu() {
    add_menu_page('AI Chatbot Settings', 'AI Chatbot', 'manage_options', 'ai-chatbot-settings', 'chatbot_settings_page');
}

// Settings page
function chatbot_settings_page() {
    ?>
    <div class="wrap">
        <h1>AI Chatbot Settings</h1>
        <form method="post" action="options.php">
            <?php
            settings_fields('chatbot_settings');
            do_settings_sections('chatbot_settings');
            submit_button();
            ?>
        </form>
    </div>
    <?php
}

// Register settings
add_action('admin_init', 'chatbot_register_settings');

function chatbot_register_settings() {
    register_setting('chatbot_settings', 'chatbot_api_url');
    add_settings_section('chatbot_main_section', 'Main Settings', null, 'chatbot_settings');
    add_settings_field('chatbot_api_url', 'API URL', 'chatbot_api_url_callback', 'chatbot_settings', 'chatbot_main_section');
}

function chatbot_api_url_callback() {
    $api_url = get_option('chatbot_api_url');
    echo "<input type='text' name='chatbot_api_url' value='$api_url' />";
}

// Add chatbot to footer
add_action('wp_footer', 'add_chatbot_to_footer');

function add_chatbot_to_footer() {
    $api_url = get_option('chatbot_api_url');
    ?>
    <div id="ai-chatbot" style="position: fixed; bottom: 20px; right: 20px; width: 300px; height: 400px; border: 1px solid #ccc; background: #fff;">
        <div id="chat-messages" style="height: 350px; overflow-y: auto; padding: 10px;"></div>
        <input type="text" id="chat-input" style="width: 80%; margin: 10px;" placeholder="Type your message...">
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
    function sendMessage() {
        var input = document.getElementById('chat-input');
        var message = input.value;
        input.value = '';

        // Display user message
        var chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML += '<p><strong>You:</strong> ' + message + '</p>';

        // Send message to API
        fetch('<?php echo $api_url; ?>', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({message: message}),
        })
        .then(response => response.json())
        .then(data => {
            // Display bot response
            chatMessages.innerHTML += '<p><strong>Bot:</strong> ' + data.response + '</p>';
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
    </script>
    <?php
}
