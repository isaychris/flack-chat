var current_channel;

document.addEventListener('DOMContentLoaded', () => {    
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    document.getElementById("new-channel-button").addEventListener("click", () => {
        console.log("button clicked")
        let channel_name = prompt("Enter a channel name")
        socket.emit('add channel', { 'channel': channel_name})
    });

    // When connected
    socket.on('connect', () => {
        if (!localStorage.getItem('display')) {
            var display = prompt("Enter a display name: ") 
            localStorage.setItem('display', display)
        }

        document.querySelector("span#display_label").innerHTML = localStorage.getItem('display');
        socket.emit('joined', { "display" : localStorage.getItem("display") });

        document.getElementById("send-button").onclick = () => {
            let text = document.querySelector('input');            
            let time = new Date();
            let current = time.getHours() + ":" + time.getMinutes();

            socket.emit('sent message', { 'user': localStorage.getItem('display'), 'time': current, 'message': text.value });
            text.value = "";
        };
        
        window.onbeforeunload = () => {
            console.log('good bye');
            socket.emit('gone', { 'display': localStorage.getItem('display') });
            return 'HUH'; 
        }
    });

    // When a new message is announced, add to chatbox
    socket.on('new message', data => {
        console.log("new message")
        let messageblock = `<article class="message">
                                <span class="user">${data["user"]}</span> <span class="time">[${data["time"]}]</span>
                                <p>${data["message"]}</p>
                            </article>`;
        document.querySelector('#messages-container').innerHTML += messageblock;

        var nodes = document.querySelectorAll('article');
        nodes[nodes.length - 1].scrollIntoView(true);

    });

    //When a online count update is announced
    socket.on('update online', data => {
        document.querySelector('#online_count').innerHTML = data["online"];
        
        if (data["event"] == "joined") {
            console.log("adding onto online list");
            var node = document.createElement("LI");
            var textnode = document.createTextNode(data['display']);
            node.appendChild(textnode);
            document.getElementById("online-list").appendChild(node);
        }

        else if (data["event"] == "gone") {
            console.log("removing from online list");
            var list = document.getElementById("online-list");
            for (i = 0; i <= list.childNodes.length; i++) {
                if (list.childNodes[i].innerHTML == data['display']) {
                    list.removeChild(list.childNodes[i]);
                    break;
                }
            }
        }
    });

    //When a online count update is announced
    socket.on('update channels', data => {            
        console.log("adding onto channel list");
        var node = document.createElement("LI");
        var textnode = document.createTextNode(data['channel']);
        node.appendChild(textnode);
        document.getElementById("channel-list").appendChild(node);
    });
});