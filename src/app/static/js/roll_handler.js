
var script_tag = document.getElementById('roll_script');
var room = script_tag.getAttribute("data-room");
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/rolls/'
    + room
 )

chatSocket.onmessage = function(event){
    let data = JSON.parse(event.data)
    console.log('Data:', data)
}

chatSocket.onclose = function(event){
    console.error('Chat socket closed unexpectedly')
}

let form = document.getElementById('websocket-form')
form.addEventListener('submit', (event)=> {
    event.preventDefault()
    let message = event.target.message.value
    chatSocket.send(JSON.stringify({
        'message': message
    }))
    form.reset()
})