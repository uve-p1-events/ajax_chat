var approve_list = [];
$tablebodyitems = $(".rwd-table>tbody");

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
    console.log("approve url is", approveMessageUrl);
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
}

function loadMessages(){
    console.log("pehele", groupList);
    $tablebodyitems.empty();

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
            $tablebodyitems.append(`<tr>
                                        <td> <input type="checkbox" name="${data.chats[i].id}" id="${data.chats[i].id}" onclick="approverFunction(${data.chats[i].id})" checked/> </td>
                                        <td> <div> ${data.chats[i].text} </div></td>
                                        <td> ${data.chats[i].owner} </td>
                                        <td> ${data.chats[i].timestamp} </td>
                                        <td> <input type="checkbox" name="${data.chats[i].id}" id="${data.chats[i].id}delete" onclick="approverFunction(${data.chats[i].id})"/> </td>
                                    </tr>
                                `);
            // $tablebodyitems.append(`<img src="/w3images/bandmember.jpg" alt="${data.chats[i].owner}" class="deltableContainer">
            //                         <p class="deltableContainer">${data.chats[i].text}
            //                         <input type="checkbox" class="deltableContainer" name="${data.chats[i].id}" id="${data.chats[i].id}" onclick="approverFunction(${data.chats[i].id})" checked/>
            //                         <b>DELETE MESSAGE ? </b>
            //                         <input type="checkbox" class="deltableContainer" name="${data.chats[i].id}" id="${data.chats[i].id}delete" onclick="approverFunction(${data.chats[i].id})"/>
            //                         </p> 
            //                         <span class="deltableContainer time-right">${data.chats[i].timestamp}</span>
            //                         <br>`);
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

// On click listener for Update button
$('#sendMsgStatus').click(function(event) {
    /* Act on the event */
    console.log("update status button clicked");
    sendAprroveStatus();
});