var approve_list = [];

function sendAprroveStatus(){
    $.ajax({
        url: approveMessageUrl,
        type: 'POST',
        dataType: 'json',
        data:{ 
                msg_data: JSON.stringify(approve_list), 
                csrfmiddlewaretoken: crsfTocken
            }
    })
    .done(function(data) {
        console.log(data);
        loadMessages();
       
    })
    .fail(function(e) {
        console.log("error is ", e);
    })

    console.log("here the approve list is ",approve_list);
}
function approverFunction(i){
    var checkBox = document.getElementById(`${i}`);
    var deletecheckBox = document.getElementById(`${i}delete`);
  
    let element = approve_list.find((e) => {
        if (e.id == i){
            return true;
        }
    });

    let temp_status = false;
    let temp_delete_status = false;
    if (checkBox.checked == true){
        temp_status = true;
        console.log(`checkboc with id ${i} is checked`);
    } else {
        temp_status = false;
        console.log(`checkboc with id ${i} is unchecked`);
    }
    if (deletecheckBox.checked == true){
        temp_delete_status = true;
        console.log(`checkboc with id ${i} is checked for deleting`);
    } else {
        temp_delete_status = false;
        console.log(`checkboc with id ${i} is unchecked for deleting`);
    }

    if(typeof(element) !== "undefined"){
        element.id = i;
        element.status = temp_status;
        element.deleteStatus = temp_delete_status;
    }else{
        let info = {
                        id: i,
                        status: temp_status,
                        deleteStatus: temp_delete_status
                   }
        approve_list.push(info);
    }
    // console.log("value of i is ", i);
}

function loadMessages(){
    // console.log(groupIdsList);
    $("img").remove(".deltableContainer");
    $("p").remove(".deltableContainer");
    $("span").remove(".deltableContainer");
    console.log("pehele", groupList);
    $.ajax({
        url: loadmessagesurl,
        type: 'POST',
        dataType: 'json',
        data:{ 
                msgLimit: msgLimitPerPage, 
                groupIds: JSON.stringify(groupList), 
                csrfmiddlewaretoken: crsfTocken
            }
    })
    .done(function(data) {
        approve_list = [];
        console.log(data);
        for(let i = 0; i<data.chats.length; i++){
            $('.container').append(`<img src="/w3images/bandmember.jpg" alt="${data.chats[i].owner}" class="deltableContainer">
                                    <p class="deltableContainer">${data.chats[i].text}
                                    <input type="checkbox" class="deltableContainer" name="${data.chats[i].id}" id="${data.chats[i].id}" onclick="approverFunction(${data.chats[i].id})" checked/>
                                    <b>DELETE MESSAGE ? </b>
                                    <input type="checkbox" class="deltableContainer" name="${data.chats[i].id}" id="${data.chats[i].id}delete" onclick="approverFunction(${data.chats[i].id})"/>
                                    </p> 
                                    <span class="deltableContainer time-right">${data.chats[i].timestamp}</span>
                                    <br>`);
            let info = {
                            id: data.chats[i].id,
                            group_id: data.chats[i].groupID,
                            status: true,
                            deleteStatus: false
                        }
            approve_list.push(info);
        }
       
    })
    .fail(function(e) {
        console.log("error is ", e);
    })
}

loadMessages();

// On click listener for Send button
$('#getmsg').click(function(event) {
    /* Act on the event */
    console.log("button is clicked get messsage");
    loadMessages();
});

$('#sendMsgStatus').click(function(event) {
    /* Act on the event */
    console.log("update status button clicked");
    sendAprroveStatus();
});


// window.document.querySelector('.typing_status').innerHTML = 'abhyam';

// window.setInterval(() => {
//     // detecting if user is not typing for more than 5 seconds.
//     if(Math.abs(new Date() - startingtime) >= 3000){
//         user_typing_status = false;
//     } 

//     $.ajax({
//         url: getChatsUrl,
//         type: 'POST',
//         dataType: 'json',
//         data:{ 
//                 typingStatus: user_typing_status, 
//                 recipient: reader, 
//                 groupFlag: onGroup, 
//                 group_id: groupId, 
//                 currentStamp: currentTimestamp, 
//                 csrfmiddlewaretoken: crsfTocken
//             }
//     })
//     .done(function(data) {
      
//         for(let i = 0; i<data.chats.length; i++){
//             $('.container').append(`<img src="/w3images/bandmember.jpg" alt="${data.chats[i].owner}" class="deltableContainer">
//                                     <p class="deltableContainer">${data.chats[i].text}</p> &nbsp
//                                     <input type="checkbox" id=${data.chats.id} onclick="myFunction()">
//                                     <span class="time-right deltableContainer">${data.chats[i].timestamp}</span>
//                                     <br>`);
//         }

           

//         if(data.group_flag == true){
//             var s = "";
//             // console.log("length of users dict", data.typing_status.length);
//             // console.log("length of users dict", data.typing_status[0].owner);
//             for (let i=0; i<data.typing_status.length; i++){
//                 if (data.typing_status[i].typingStatus == true){
//                     s = s + `${data.typing_status[i].owner} `;
//                     console.log(`====== => ${data.typing_status[i].owner}`);
//                 }
                
//             }

//             if (s != ""){
//                 window.document.querySelector('.typing_status').innerHTML = `users typing are => ${s}`;
//             }else{
//                 window.document.querySelector('.typing_status').innerHTML = s;
//             }
//             // console.log(`users typing are => ${data.typing_status[0].owner}`);
//         }else{
//             if(data.typing_status == true){
//                 window.document.querySelector('.typing_status').innerHTML = `user : ${reader} is typing`;
//             }else{
//                 window.document.querySelector('.typing_status').innerHTML = "";
//             }
//             console.log(`users ${reader} typing status => ${data.typing_status}`);
//         }
//     })
//     .fail(function(e) {
//         console.log("error is ", e);
//     })
//   },1000);
