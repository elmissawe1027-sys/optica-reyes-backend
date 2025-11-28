let usuarioEstaLogueado = false;

function mostrarSeccion(id) {
    const esSeccionProtegida = (id !== 'inicio' && id !== 'registro');
    if (esSeccionProtegida && !usuarioEstaLogueado) {
        alert('¡Necesitas iniciar sesión para ver esta sección!');
        return; 
    }
    const secciones = document.querySelectorAll('section');
    secciones.forEach(sec => sec.classList.remove('active'));
    const seccionActiva = document.getElementById(id);
    if (seccionActiva) {
        seccionActiva.classList.add('active');
    }
}

function comprarProducto(nombre, precio) {
    document.getElementById('compra-producto-nombre').innerText = nombre;
    document.getElementById('compra-producto-precio').innerText = precio;
    mostrarSeccion('compra');
}

function cerrarSesion() {
    usuarioEstaLogueado = false; 
    document.getElementById('navegacion-principal').style.display = 'none';
    document.getElementById('user-profile-area').style.display = 'none';
    document.getElementById('user-menu-dropdown').classList.remove('show-dropdown');
    mostrarSeccion('inicio');
}

function toggleUserMenu(event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    document.getElementById('user-menu-dropdown').classList.toggle('show-dropdown');
}

window.onclick = function(event) {
    if (!event.target.matches('#user-menu-button')) {
        const dropdowns = document.getElementsByClassName("show-dropdown");
        for (let i = 0; i < dropdowns.length; i++) {
            dropdowns[i].classList.remove('show-dropdown');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {

    const formReseña = document.getElementById('form-reseña');
    if (formReseña) {
        formReseña.addEventListener('submit', (evento) => {
            evento.preventDefault(); 
            alert('¡Gracias por tu reseña!');
            formReseña.reset();
        });
    }

    const formCompra = document.getElementById('form-compra');
    if (formCompra) {
        formCompra.addEventListener('submit', async (evento) => {
            evento.preventDefault(); 
            const nombreCliente = document.getElementById('compra_nombre').value;
            const email = document.getElementById('compra_email').value;
            const direccion = document.getElementById('compra_direccion').value;
            const tarjeta = document.getElementById('compra_tarjeta').value; 
            const productoNombre = document.getElementById('compra-producto-nombre').innerText;
            const productoPrecio = document.getElementById('compra-producto-precio').innerText;
            const datosDelPedido = {
                cliente: nombreCliente,
                email: email,
                direccion: direccion,
                tarjeta: tarjeta, 
                producto: productoNombre,
                precio: productoPrecio,
            };
            try {
                const respuesta = await fetch('http://127.0.0.1:8000/api/crear-pedido/', { 
                    method: 'POST', 
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(datosDelPedido) 
                });
                if (respuesta.ok) {
                    const data = await respuesta.json(); 
                    alert('¡Gracias por tu compra! ID Pedido: ' + data.pedido_id);
                    formCompra.reset();
                    mostrarSeccion('inicio');
                } else {
                    alert('Hubo un error con tu pedido.');
                }
            } catch (error) {
                alert('No se pudo conectar con el servidor.');
            }
        });
    }

    const formRegistro = document.getElementById('form-registro');
    if (formRegistro) {
        formRegistro.addEventListener('submit', async (evento) => {
            evento.preventDefault();
            const usuario = document.getElementById('reg_usuario').value;
            const email = document.getElementById('reg_email').value;
            const password = document.getElementById('reg_password').value;
            const password2 = document.getElementById('reg_password2').value;
            if (password !== password2) {
                alert('Las contraseñas no coinciden.');
                return; 
            }
            const datosRegistro = {
                username: usuario,
                email: email,
                password: password
            };
            try {
                const respuesta = await fetch('http://127.0.0.1:8000/api/registrar/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(datosRegistro)
                });
                if (respuesta.ok) {
                    alert('¡Usuario registrado con éxito! Ahora inicia sesión.');
                    formRegistro.reset();
                    mostrarSeccion('inicio');
                } else {
                    alert('Error al registrar. El usuario o email ya podría existir.');
                }
            } catch (error) {
                alert('No se pudo conectar con el servidor.');
            }
        });
    }

    const formInicio = document.getElementById('form-inicio');
    if (formInicio) {
        formInicio.addEventListener('submit', async (evento) => {
            evento.preventDefault();
            const usuario = document.getElementById('usuario').value;
            const password = document.getElementById('password').value;
            const datosLogin = { username: usuario, password: password };

            try {
                const respuesta = await fetch('http://127.0.0.1:8000/api/login/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(datosLogin)
                });
                if (respuesta.ok) {
                    const data = await respuesta.json();
                    usuarioEstaLogueado = true; 
                    
                    document.getElementById('navegacion-principal').style.display = 'block'; 
                    const profileArea = document.getElementById('user-profile-area');
                    profileArea.style.display = 'flex';
                    document.getElementById('user-display-name').innerText = data.username;
                    const cardNombre = document.getElementById('card-nombre');
                    if(cardNombre) cardNombre.innerText = data.username;
                    
                    alert('¡Bienvenido, ' + data.username + '!');
                    formInicio.reset();
                    mostrarSeccion('armazones'); 
                } else {
                    alert('Usuario o contraseña incorrectos.');
                }
            } catch (error) {
                alert('No se pudo conectar con el servidor.');
            }
        });
    }

    const formPerfil = document.getElementById('form-perfil');
    if (formPerfil) {
        formPerfil.addEventListener('submit', async (evento) => {
            evento.preventDefault();
            const usuario = document.getElementById('perfil_usuario').value;
            const email = document.getElementById('perfil_email').value;
            
            const formData = new FormData();
            if (usuario.trim() !== "") formData.append('username', usuario);
            if (email.trim() !== "") formData.append('email', email);
            
            try {
                const respuesta = await fetch('http://127.0.0.1:8000/api/actualizar-perfil/', {
                    method: 'POST',
                    body: formData 
                });
                if (respuesta.ok) {
                    const data = await respuesta.json();
                    alert('¡Perfil actualizado con éxito!');
                    if (data.username) {
                        document.getElementById('user-display-name').innerText = data.username;
                        document.getElementById('card-nombre').innerText = data.username;
                    }
                    formPerfil.reset();
                } else {
                    alert('Error al actualizar.');
                }
            } catch (error) {
                alert('No se pudo conectar con el servidor.');
            }
        });
    }

    const inputFoto = document.getElementById('input-foto-oculto');
    if (inputFoto) {
        inputFoto.addEventListener('change', async () => {
            if (inputFoto.files && inputFoto.files[0]) {
                const formData = new FormData();
                formData.append('imagen', inputFoto.files[0]);
                
                const usuarioActual = document.getElementById('user-display-name').innerText;
                formData.append('username', usuarioActual); 

                try {
                    const res = await fetch('http://127.0.0.1:8000/api/actualizar-perfil/', {
                        method: 'POST', body: formData
                    });
                    
                    if(res.ok) {
                        const data = await res.json();
                        if(data.imagen_url) {
                            document.getElementById('img-avatar-visual').src = data.imagen_url + '?t=' + new Date().getTime();
                        }
                    } else {
                        const errorData = await res.json();
                        alert('Error: ' + (errorData.error || 'No se pudo subir la foto'));
                    }
                } catch(err) { 
                    alert('Error de conexión.'); 
                }
            }
        });
    }

    const formPassword = document.getElementById('form-password');
    if (formPassword) {
        formPassword.addEventListener('submit', async (evento) => {
            evento.preventDefault();
            const actual = document.getElementById('pass_actual').value;
            const nueva = document.getElementById('pass_nueva').value;
            const confirmar = document.getElementById('pass_confirmar').value;
            if (nueva !== confirmar) {
                alert('Las nuevas contraseñas no coinciden.');
                return;
            }
            const datosPassword = {
                old_password: actual,
                new_password: nueva
            };
            try {
                const respuesta = await fetch('http://127.0.0.1:8000/api/cambiar-password/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(datosPassword)
                });
                if (respuesta.ok) {
                    alert('¡Contraseña cambiada con éxito!');
                    formPassword.reset();
                } else {
                    alert('Error al cambiar la contraseña. Verifica tu contraseña actual.');
                }
            } catch (error) {
                alert('No se pudo conectar con el servidor.');
            }
        });
    }

});