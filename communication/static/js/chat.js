// initialising all the local variables
var user_typing_status = false;
var startingtime = new Date();
var latestChat;
var oldestChat;

// function to send the user input message to server with passing all other required variables and parameters by "POST" request
function sendMessage(){
    text=$('#msg').val();
    if (text.length>0) {
        $.ajax({
        url: logMsg,
        type: 'POST',
        dataType: 'json',
        data:{
                msg: text, 
                owner: sessionOwner, 
                recipient: reader, 
                groupFlag: onGroup, 
                group_id: groupId, 
                currentStamp: currentTimestamp,
                group_protection: groupProtection,  
                csrfmiddlewaretoken: crsfTocken
            }
        })
        .done(function(data) {
            $('#msg').val('');
            console.log("data is ", data);
        })
        .fail(function() {
            console.log("error");
        })
    }
}


// enter key listener. Send the message typed in message box to server if enter key is pressed by calling sendMessage function.
window.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
}, false);

// On click listener for Send button
$('#btn').click(function(event) {
    /* Act on the event */
    sendMessage();
});

// On click listener for load message button.
$("#loadMessage").click(function(event){
    var oldChatTempDict = {
                            group_id: oldestChat.groupId,
                            id: oldestChat.id,
                            is_group: oldestChat.isGroup,
                            owner: oldestChat.owner,
                            recipient: oldestChat.recipient,
                            text: oldestChat.text,
                            normal_timestamp: oldestChat.normalTimestamp
                          };
    $.ajax({
        url: loadmessagesurl,
        type: 'POST',
        dataType: 'json',
        data:{
                dataObject: JSON.stringify(oldChatTempDict),
                recipient: reader, 
                groupFlag: onGroup, 
                group_id: groupId, 
                csrfmiddlewaretoken: crsfTocken
            }
        })
        .done(function(data) {
            // console.log("data is ", data);
            if (data.chats.length == 0){
                window.alert("No more messages to load");
            }
            for(let i = data.chats.length-1; i>=0; i--){
                $('.container').prepend(`<img src="/w3images/bandmember.jpg" alt="${data.chats[i].owner}" class="deltableContainer">
                                         <p class="deltableContainer">${data.chats[i].text}</p>
                                         <span class="time-right deltableContainer">${data.chats[i].timestamp}</span>`);
            }

            // initialising the oldest chat variable with the oldest message object recieved when the server sends the list of 20 messages after requesting.
            if (data.chats.length != 0){
                oldestChat = data.chats[0];
            }
        })
        .fail(function() {
            console.log("error");
        })
    console.log(oldestChat);
});


// setting on typing listener on message box and initiallising the required variables to update the user status as typing or not
const input = document.querySelector('#msg');
input.addEventListener("input", function(s) {
    console.log("user is typing");
    user_typing_status = true;
    startingtime = new Date();
});

// window.document.querySelector('.typing_status').innerHTML = 'abhyam';

window.setInterval(() => {
    // detecting if user is not typing for more than 5 seconds.
    if(Math.abs(new Date() - startingtime) >= 3000){
        user_typing_status = false;
    } 

    $.ajax({
        url: getChatsUrl,
        type: 'POST',
        dataType: 'json',
        data:{ 
                typingStatus: user_typing_status, 
                recipient: reader, 
                groupFlag: onGroup, 
                group_id: groupId, 
                currentStamp: currentTimestamp, 
                csrfmiddlewaretoken: crsfTocken
            }
    })
    .done(function(data) {
        // $("img").remove(".deltableContainer");
        // $("p").remove(".deltableContainer");
        if (typeof(latestChat) !== "undefined"){
        // $("span").remove(".deltableContainer");
            console.log("executed from length >0");
            console.log("from >0 value of latestchat is", latestChat);
            
            let chatIndex = data.chats.findIndex((element) => {
                if(element.id == latestChat.id && element.owner == latestChat.owner && element.groupId == latestChat.groupId && element.text == latestChat.text && element.isgroup == latestChat.isgroup){
                    return true;
                }else{
                    return false;
                }
            });

            console.log("last index is", chatIndex);
            console.log("chats list is =>", data.chats);
            console.log("chats list length is =>", data.chats.length);
            for(let i = chatIndex+1 ;i<data.chats.length; i++){
                $('.container').append(`<img src="/w3images/bandmember.jpg" alt="${data.chats[i].owner}" class="deltableContainer">
                                        <p class="deltableContainer">${data.chats[i].text}</p>
                                        <span class="time-right deltableContainer">${data.chats[i].timestamp}</span>`);
            }

            if(data.chats.length != 0){
                latestChat = data.chats[data.chats.length -1];
            }

        }else{
            console.log("executed from length =0");
            for(let i = 0; i<data.chats.length; i++){
                $('.container').append(`<img src="/w3images/bandmember.jpg" alt="${data.chats[i].owner}" class="deltableContainer">
                                        <p class="deltableContainer">${data.chats[i].text}</p>
                                        <span class="time-right deltableContainer">${data.chats[i].timestamp}</span>`);
            }

            if(data.chats.length != 0){
                oldestChat = data.chats[0];
                latestChat = data.chats[data.chats.length -1];
            }
        }

        if(data.group_flag == true){
            var s = "";
            // console.log("length of users dict", data.typing_status.length);
            // console.log("length of users dict", data.typing_status[0].owner);
            for (let i=0; i<data.typing_status.length; i++){
                if (data.typing_status[i].typingStatus == true){
                    s = s + `${data.typing_status[i].owner} `;
                    console.log(`====== => ${data.typing_status[i].owner}`);
                }
                
            }

            if (s != ""){
                window.document.querySelector('.typing_status').innerHTML = `users typing are => ${s}`;
            }else{
                window.document.querySelector('.typing_status').innerHTML = s;
            }
            // console.log(`users typing are => ${data.typing_status[0].owner}`);
        }else{
            if(data.typing_status == true){
                window.document.querySelector('.typing_status').innerHTML = `user : ${reader} is typing`;
            }else{
                window.document.querySelector('.typing_status').innerHTML = "";
            }
            console.log(`users ${reader} typing status => ${data.typing_status}`);
        }
    })
    .fail(function(e) {
        console.log("error is ", e);
    })
  },1000);
