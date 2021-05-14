// alert('{{ STATIC_URL|escapejs }}');
function sendMessage(){
    text=$('#msg').val();
    if (text.length>0) {
        $.ajax({
        url: logMsg,
        type: 'POST',
        dataType: 'json',
        data: {msg: text, owner: sessionOwner, recipient: reader, groupFlag: onGroup, group_id: groupId, currentStamp: currentTimestamp, csrfmiddlewaretoken: crsfTocken}
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

// enter key listener
window.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
}, false);

$('#btn').click(function(event) {
    /* Act on the event */
    sendMessage();
});

$.ajax({
        url: getChatsUrl,
        type: 'POST',
        dataType: 'json',
        data: {typingStatus: false, recipient: reader, groupFlag: onGroup, group_id: groupId, currentStamp: currentTimestamp, csrfmiddlewaretoken: crsfTocken}
    })
    .done(function(data) {
        console.log("mai hu sperman");
        console.log(data);
        console.log(data.chats);
    })
    .fail(function(error) {
        console.log("error is 1", error);
    })

var user_typing_status = false;
const input = document.querySelector('#msg');

var startingtime = new Date();
input.addEventListener("input", function(s) {
    console.log("user is typing");
    user_typing_status = true;
    startingtime = new Date();
});

// window.document.querySelector('.typing_status').innerHTML = 'abhyam';

window.setInterval(() => {
    // detecting if user is not typing for more than 5 seconds.
    if(Math.abs(new Date() - startingtime)> 3000){
        user_typing_status = false;
    } 

    $.ajax({
        url: getChatsUrl,
        type: 'POST',
        dataType: 'json',
        data: {typingStatus: user_typing_status, recipient: reader, groupFlag: onGroup, group_id: groupId, currentStamp: currentTimestamp, csrfmiddlewaretoken: crsfTocken}
    })
    .done(function(data) {
        $("img").remove(".deltableContainer");
        $("p").remove(".deltableContainer");
        $("span").remove(".deltableContainer");
        for(let i = 0;i<data.chats.length;i++){
            $('.container').append(`<img src="/w3images/bandmember.jpg" alt="${data.chats[i].owner}" class="deltableContainer">
                                    <p class="deltableContainer" >${data.chats[i].text}</p>
                                    <span class="time-right deltableContainer">${data.chats[i].timestamp}</span>`);

        }

        if(data.group_flag == true){
            var s = "";
            console.log("length of users dict", data.typing_status.length);
            // console.log("length of users dict", data.typing_status[0].owner);
            for (let i=0; i<data.typing_status.length; i++){
                if (data.typing_status[i].typingStatus == true){
                    s = s + `user ${data.typing_status[i].owner} is typing `;
                    console.log(`====== => ${data.typing_status[i].owner}`);
                }
                
            }
            if (s!=""){
                window.document.querySelector('.typing_status').innerHTML = `users typing are => ${s}`;
            }
            else{
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
