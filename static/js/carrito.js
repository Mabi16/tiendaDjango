var actualizarBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < actualizarBtns.length; i++) {
    actualizarBtns[i].addEventListener('click', function(){
        var productoId = this.dataset.producto
        var action = this.dataset.action
        console.log('productoID: ', productoId, 'Action:', action)

        console.log('USUARIO: ',usuario)
        if (usuario == 'AnonymousUser') {
            console.log('No hay sesion iniciada');
        }else{
            actualizarPedidoUsuario(productoId, action)
        }
    })
    
}

function actualizarPedidoUsuario(productoId,action) {
    console.log('Usuario iniciado, mandando datos...');

    var url = '/actualizar_articulo/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body:JSON.stringify({
            'productoId': productoId, 'action':action
        })
    })
    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data: ',data)
        location.reload()
    })
}