$('#btn').click(function(event) {
    /* Act on the event */
    console.log("button is clocked");
    text=$('#msg').val();
    if (text.length>0) {
        $.ajax({
        url: '{% url "logMessage" %}',
        type: 'POST',
        dataType: 'json',
        data: {msg: text, owner:"abhyam",csrfmiddlewaretoken:"{{csrf_token}}"}
        })
        .done(function(data) {
            $('#msg').val('');
            console.log("data is ", data);
        })
        .fail(function() {
            console.log("error");
        })
    }
});


$.ajax({
    url:'{% url "getChats" %}',
    type: 'POST',
    dataType: 'json',
    data: {csrfmiddlewaretoken:"{{csrf_token}}"}
})
.done(function(data) {
    console.log("mai hu sperman");
    console.log(data);
    console.log(data[0]);
})
.fail(function(error) {
    console.log("error is", error);
})

window.setInterval(() => {
    $.ajax({
        url:'{% url "getChats" %}',
        type: 'POST',
        dataType: 'json',
        data: {csrfmiddlewaretoken:"{{csrf_token}}"}
    })
    .done(function(data) {
        $("img").remove(".deltableContainer");
        $("p").remove(".deltableContainer");
        $("span").remove(".deltableContainer");
        for(let i = 0;i<data.length;i++){
            $('.container').append(`<img src="/w3images/bandmember.jpg" alt="${data[i].owner}" class="deltableContainer">
                                    <p class="deltableContainer" >${data[i].text}</p>
                                    <span class="time-right deltableContainer">${data[i].timestamp}</span>`);

            console.log(`id=> ${data[i].id}, text => ${data[i].text}, owner => ${data[i].owner}`)
        }
    })
    .fail(function() {
        console.log("error");
    })
  },1000);