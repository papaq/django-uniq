function scrollDown(element_id){
    var element=document.getElementById(element_id);
    element.scrollTop = element.scrollHeight;
}

var timer = null;

function updateMessages(){
    timer = setInterval( getMessages , 2000 );
}

$(document).on('onbeforeunload', '#index', function(){
    clearInterval(timer);
});

/*
window.onbeforeunload = function () {
    clearInterval(timer)
};
*/

//$("#id_username").change(function () {

function getMessages() {
    var url = window.location.href.split('/');
    var dialogue = url[url.length - 2];
    var messages_number = $('#messages_list').children().length;

    $.ajax({
        type : 'GET',
        url : '/dialogue/ajax/get_messages/',
        dataType : 'html',
        data: {
            'dialogue': dialogue,
            'messages_number': messages_number
        },
        success : function(data){
            $('#messages_list').append(data)
        }
    });
}

