let url = 'ws://localhost:8000/ws/socket-server'

const chatSocket = new WebSocket(url)

chatSocket.onmessage = function(event){
    let data = JSON.parse(event.data)
    console.log('Data:', data)
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