
var script_tag = document.getElementById('roll_script')
var room = script_tag.getAttribute("data-room")
var user = script_tag.getAttribute("data-user")
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/rolls/'
    + room
 )
const log = document.getElementById('dicelog')

chatSocket.onmessage = function(event){
    let data = JSON.parse(event.data)
    console.log('Data:', data)
    log.innerHTML += `<div class="cell">` + data.user + ': ' + data.roll + `</div>` // outputs the roll to the log element
    log.scrollTop = log.scrollHeight // scrolls to the bottom of the log automatically
}

chatSocket.onclose = function(event){
    console.error('Chat socket closed unexpectedly')
}

let form = document.getElementById('websocket-form')
form.addEventListener('submit', (event)=> {
    event.preventDefault()
    let message = event.target.message.value
    chatSocket.send(JSON.stringify({
        'message': message,
        'user': user
    }))
    form.reset()
})