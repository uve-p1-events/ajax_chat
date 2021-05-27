$(document).ready(function () {
    var user_typing_status = false;
    var startingtime = new Date();
    var latestChat;
    var oldestChat; 
    var chatsFetcher;
    var $chatHistory = $(".chat-history");
    var $chatHistoryList = $chatHistory.find("ul");
    var $activeUserHeadName = $(".chat-with");
    var $activeUserTypingStatus = $(".chat-num-messages");
    // variables for particular active chat user.
    var recipient = "";
    var onGroup = false;
    var group_id = ""; 
    var currentStamp = new Date();
    var group_protection = false;   

    // console.log($activeUserHeadName.text("hello"));
    function scrollToBottom() {
        $chatHistory.scrollTop($chatHistory[0].scrollHeight);
    }

    function scrollToTop() {
        $chatHistory.scrollTop(0);
    }

    function appendMessages(data, startindex, endindex){
        for(let i = startindex; i<endindex; i++){
            // console.log(`${data.chats[i].owner} + ${data.chats[i].text} + ${data.chats[i].timestamp}`);
            // console.log(`owner is ${data.chats[i].owner} and session owner is ${sessionOwner}`);
            if(data.chats[i].owner != sessionOwner){
                $chatHistoryList.append(
                    `<li>
                        <div class="message-data">
                            <span class="message-data-name"></i>${data.chats[i].owner}</span>
                            <span class="message-data-time">${data.chats[i].timestamp}</span>
                        </div>
                        <div class="message my-message">
                            ${data.chats[i].text} 
                        </div>
                    </li>`
                );
            }
            else{
                $chatHistoryList.append(
                    `<li class="clearfix">
                        <div class="message-data align-right">
                            <span class="message-data-time" >${data.chats[i].timestamp}</span>
                            <span class="message-data-name" >${data.chats[i].owner}</span>
                        </div>
                        <div class="message other-message float-right">
                            ${data.chats[i].text} 
                        </div>
                    </li>`
                );
            }
        }
        console.log("chat histiry item is ", $chatHistory);
        console.log("chat histiry item is woth 0", $chatHistory[0]);
        scrollToBottom();
    }

    function fetchMessages(reader, onGroup, groupId, currentTimestamp) {
        chatsFetcher = window.setInterval(() => {
            // console.log("value of griupd is ", groupId);
            // detecting if user is not typing for more than 5 seconds.
            if(Math.abs(new Date() - startingtime) >= 2000){
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
                if (latestChat !== "undefined"){
                    // console.log("executed from length >0");
                    // console.log("from >0 value of latestchat is", latestChat);
                    
                    let chatIndex = data.chats.findIndex((element) => {
                        if(element.id == latestChat.id && element.owner == latestChat.owner && element.groupId == latestChat.groupId && element.text == latestChat.text && element.isgroup == latestChat.isgroup){
                            return true;
                        }else{
                            return false;
                        }
                    });
        
                    // console.log("last index is", chatIndex);
                    // console.log("chats list is =>", data.chats);
                    // console.log("chats list length is =>", data.chats.length);
                    if (chatIndex+1 !== data.chats.length){
                        appendMessages(data, chatIndex+1, data.chats.length);
                    }
        
                    if(data.chats.length != 0){
                        latestChat = data.chats[data.chats.length -1];
                    }
        
                }else{
                    // console.log("executed from length =0");
                    appendMessages(data, 0, data.chats.length);
        
                    if(data.chats.length != 0){
                        oldestChat = data.chats[0];
                        latestChat = data.chats[data.chats.length -1];
                    }

                    // console.log("oldestChat is ==>" , oldestChat);
                    // console.log("latestChat is ==>" , latestChat);
                }
        
                if(data.group_flag == true){
                    var s = "";
                    // console.log("length of users dict", data.typing_statuser('input', updateValue);.length);
                    // console.log("length of users dict", data.typing_status[0].owner);

                    // for (let i=0; i<data.typing_status.length; i++){
                    //     if (data.typing_status[i].typingStatus == true){
                    //         s = s + `${data.typing_status[i].owner} `;
                    //         console.log(`====== => ${data.typing_status[i].owner}`);
                    //     }
                        
                    // }
        
                    // if (s != ""){
                    //     window.document.querySelector('.typing_status').innerHTML = `users typing are => ${s}`;
                    // }else{
                    //     window.document.querySelector('.typing_status').innerHTML = s;
                    // }

                    // console.log(`users typing are => ${data.typing_status[0].owner}`);

                }else{
                    if(data.typing_status == true){
                        $activeUserTypingStatus.text("Typing...");
                    }else{
                        $activeUserTypingStatus.text("");
                    }
                    // console.log(`users ${reader} typing status => ${data.typing_status}`);
                }
            })
            .fail(function(e) {
                console.log("error occured while fetching messagess! => ", e);
            })
        },1000);
    }

    function loadMoreMessagesFunction(){
        let oldChatTempDict = {
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
                    recipient: recipient, 
                    groupFlag: onGroup, 
                    group_id: group_id, 
                    csrfmiddlewaretoken: crsfTocken
                }
            })
            .done(function(data) {
                // console.log("data is ", data);
                if (data.chats.length == 0){
                    window.alert("No more messages to load");
                }
                for(let i = data.chats.length-1; i>=0; i--){
                    if(data.chats[i].owner != sessionOwner){
                        $chatHistoryList.prepend(
                            `<li>
                                <div class="message-data">
                                    <span class="message-data-name"></i>${data.chats[i].owner}</span>
                                    <span class="message-data-time">${data.chats[i].timestamp}</span>
                                </div>
                                <div class="message my-message">
                                    ${data.chats[i].text} 
                                </div>
                            </li>`
                        );
                    }
                    else{
                        $chatHistoryList.prepend(
                            `<li class="clearfix">
                                <div class="message-data align-right">
                                    <span class="message-data-time" >${data.chats[i].timestamp}</span>
                                    <span class="message-data-name" >${data.chats[i].owner}</span>
                                </div>
                                <div class="message other-message float-right">
                                    ${data.chats[i].text} 
                                </div>
                            </li>`
                        );
                    }
                }
                
                // now scrolling to top messages
                scrollToTop();
                // initialising the oldest chat variable with the oldest message object recieved when the server sends the list of 20 messages after requesting.
                if (data.chats.length != 0){
                    oldestChat = data.chats[0];
                }
            })
            .fail(function() {
                console.log("error");
            })
        // console.log(oldestChat);
        // console.log("hello");
    }

    // listener for load more messages
    $("#loadOldMessages").on("click", loadMoreMessagesFunction.bind(this));

    var chat = {
        messageToSend: "",
        init: function () {
            this.cacheDOM();
            this.bindEvents();
        },
        cacheDOM: function () {
            // this.$chatHistory = $(".chat-history");
            this.$button = $("button");
            this.$textarea = $("#message-to-send");
            this.$user = document.querySelectorAll('.single-user');
            this.$userProfileAvatar = $(".active-user-logo");
            // this.$chatHistoryList = this.$chatHistory.find("ul");
        },

        bindEvents: function () {
            this.$button.on("click", this.addMessage.bind(this));
            this.$textarea.on("keyup", this.addMessageEnter.bind(this));
            this.$textarea.on("input", this.typingStatusManager.bind(this));
            this.$user.forEach((u) => {
                u.addEventListener('mousedown', () => {
                    this.showUserChats(u)
                })
            });
        },

        typingStatusManager: function () {
            console.log("User is typing");
            user_typing_status = true;
            startingtime = new Date();
        },

        showUserChats: function(clicked_user){
            $chatHistoryList.empty();           // clearing the pre exsisting items in chat field.                                               
            user_typing_status = false;         // for typing status
            startingtime = new Date();          // variable for typing status
            latestChat = "undefined";                    
            oldestChat = "undefined"; 
            clearInterval(chatsFetcher);        // for clearing the message recieve infinite listener on particular chat
            let otherUserName = clicked_user.innerText.split("\n")[0];
            $activeUserHeadName.text(otherUserName);            // setting the username for Active user which is currently selected on screen.
            this.$userProfileAvatar.attr("src", `https://avatars.dicebear.com/api/human/${otherUserName}.svg`)
            this.getChatUserInfoRequester(otherUserName);       // for recieving details about the selected active user.
            // console.log(clicked_user.innerText.split("\n")[0]);
        },

        getChatUserInfoRequester: function (otherusername) {
            $.ajax({
                url: getChatUserInfo,
                type: 'POST',
                dataType: 'json',
                data:{
                        user: otherusername,
                        csrfmiddlewaretoken: crsfTocken
                    }
                })
                .done(function(data) {
                    console.log(data);
                    recipient = data.reader;
                    onGroup = data.onGroup;
                    group_id = data.groupId;
                    currentTimestamp = data.currentTimestamp;
                    groupProtection = false;
                    console.log("value of group id in fetching msgs is ", group_id);
                    console.log("value of reciept in fetching msgs is ", recipient);
                    fetchMessages(data.reader, data.onGroup, data.groupId, data.currentTimestamp);
                        
                })
                .fail(function() {
                    console.log("error faced while fetching data of getChatUserInfo");
                })
        },

        logMessage: function () {
            this.scrollToBottom();
            console.log("value of group id is ", group_id);
            console.log("value of recipt is ", recipient);
            if (this.messageToSend.trim() !== "") {
                $.ajax({
                    url: logMsg,
                    type: 'POST',
                    dataType: 'json',
                    data:{
                            msg: this.messageToSend.trim(), 
                            owner: sessionOwner, 
                            recipient: recipient, 
                            groupFlag: onGroup, 
                            group_id: group_id, 
                            currentStamp: currentTimestamp,
                            group_protection: group_protection,
                            csrfmiddlewaretoken: crsfTocken
                        }
                    })
                    .done(function(data) {
                        $('#msg').val('');
                        console.log("data is ", data);
                    })
                    .fail(function(e) {
                        console.log("error occured while sending message and the error is");
                        console.log(e);
                    })

                this.$textarea.val("");
            }
        },

        addMessage: function() {
            // console.log(this.$textarea);
            this.messageToSend = this.$textarea.val()
            this.logMessage();
        },

        addMessageEnter: function (event) {
            // enter was pressed
            if (event.keyCode === 13) {
                this.addMessage();
            }
        },
        scrollToBottom: function () {
            $chatHistory.scrollTop($chatHistory[0].scrollHeight);
        },

        getCurrentTime: function () {
            return new Date()
                .toLocaleTimeString()
                .replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3");
        },

        getRandomItem: function (arr) {
            return arr[Math.floor(Math.random() * arr.length)];
        },

    };

    chat.init();

    var searchFilter = {
        options: {
            valueNames: ["name"]
        },
        init: function () {
            var userList = new List("people-list", this.options);
            var noItems = $('<li id="no-items-found">No items found</li>');

            userList.on("updated", function (list) {
                if (list.matchingItems.length === 0) {
                    $(list.list).append(noItems);
                } else {
                    noItems.detach();
                }
            });
        }
    };

    // searchFilter.init();
    
});

// document.querySelector('.chat[data-chat=person2]').classList.add('active-chat')
// document.querySelector('.person[data-chat=person2]').classList.add('active')

// let friends = {
//     list: document.querySelector('ul.people'),
//     all: document.querySelectorAll('.left .person'),
//     name: ''
//   },
//   chat = {
//     container: document.querySelector('.container .right'),
//     current: null,
//     person: null,
//     name: document.querySelector('.container .right .top .name')
//   }

// friends.all.forEach(f => {
//   f.addEventListener('mousedown', () => {
//     f.classList.contains('active') || setAciveChat(f)
//   })
// });

// function setAciveChat(f) {
//   friends.list.querySelector('.active').classList.remove('active')
//   f.classList.add('active')
//   chat.current = chat.container.querySelector('.active-chat')
//   chat.person = f.getAttribute('data-chat')
//   chat.current.classList.remove('active-chat')
//   chat.container.querySelector('[data-chat="' + chat.person + '"]').classList.add('active-chat')
//   friends.name = f.querySelector('.name').innerText
//   chat.name.innerHTML = friends.name
// }