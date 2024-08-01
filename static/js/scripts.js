// al presionar el boton se recarga la pagina mostrando la imagen recibida
document.addEventListener("DOMContentLoaded", function() {
  const reloadButton = document.getElementById("reload-button");

  reloadButton.addEventListener("click", () =>  {
      this.location.reload(); 
  });
});


function aplicarFiltro() {
    
    fetch('/aplicar_filtro', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mensaje: "Aplicar filtro" })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        
        console.log("aplicar filtro");;
    })
    .catch((error) => {
        console.error('Error:', error);
    });

    this.location.reload(); 
}
