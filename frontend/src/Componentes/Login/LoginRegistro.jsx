import React, { useState, useEffect  } from 'react';
import './LoginRegistro.css'
import { RiLockPasswordFill  } from "react-icons/ri";
import { IoMdMail } from "react-icons/io";
import { FaUserAlt } from "react-icons/fa";
import { IoIosEye, IoIosEyeOff  } from "react-icons/io";
import { FaUserAstronaut } from "react-icons/fa6";

//import logo from "../Assets/PC_logo.png"
import {  useNavigate } from 'react-router-dom';
import Alert from '@mui/material/Alert';
// URL base del backend
const BASE_URL = 'http://localhost:8000'

const LoginRegistro = () => {

  /*Para cambiar la pantalla entre el inicio de sesion y el registro */
  const [action,setAction]= useState('');

  const registrarse = () => {
    setAction(' active')
  }

  const login = () => {
    setAction('')
  }

  const navigate = useNavigate(); // Obtiene el objeto history para navegar entre rutas
  /*toggle para pinchar en el ojo y que enseñe la contraseña*/
  const [passwordVisible, setShowPassword] = useState(false);

  const togglePasswordVisibility = () => {
    setShowPassword(!passwordVisible);
  }
  const [alert, setAlert] = useState({ severity: '', message: '' });

  useEffect(() => {
    // Verificar si hay un token guardado al cargar la página
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      console.log('Sesión iniciada. Redireccionando a la página de inicio...');
      console.log("Es un Usuario")
      navigate("/Inicio"); // enviamos al incio
    } else {
      console.log('Sesión NO iniciada.');
    }
  }, []);

  // Fetch Login
  const loginEP = async (event) => {
    event.preventDefault();
    const { sobrenom, contrasenya } = event.target.elements;
    
    if (!sobrenom || !contrasenya) {
      console.error('Faltan campos');
      return;
    }

    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        sobrenom: sobrenom.value,
        contrasenya: contrasenya.value,
      }),
    });
    
    const data = await response.json();
    console.log(data)
    if (response.ok) {
        localStorage.setItem("token",data.access_token);
        localStorage.setItem("sobrenom", sobrenom.value); 
      console.log('Sesión iniciada. Redireccionando a la página de inicio...');
        console.log("Bienvenido")
        navigate("/Inicio"); // enviamos al incio
    } else {
      // Manejar error de inicio de sesión
      console.error('Error al iniciar sesión:', data.message);
      setAlert({ severity: 'error', message: 'Error al iniciar sesión, Error: '+ data.detail });

    }
  };

  // Fetch registro
  const registrarseEP = async (event) => {
    event.preventDefault();
    // Obtener los valores de los campos del formulario
    const { nom, email, contrasenya,sobrenom, datanaixement } = event.target.elements;
    if (!nom ||!email || !contrasenya||!sobrenom || !datanaixement) {
      console.error('No se pueden encontrar los campos necesarios para el registro');
      return;
    }
    // Hacer la solicitud de registro al backend
    try {
      const response = await fetch(`${BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nom: nom.value,
          datanaixement: datanaixement.value,
          correuelectronic:email.value ,
          contrasenya: contrasenya.value,
          sobrenom: sobrenom.value,
          }),
      });

      // Verificar el estado de la respuesta
      if (response.ok) {
        // Registro exitoso
        console.log('Registro exitoso');
        window.location.reload();// enviamos al login nuevamente
      } else {
        const errorData = await response.json();
        console.error('Error en el registro:', errorData.message);
        setAlert({ severity: 'error', message: 'Error al iniciar sesión, Error: '+ errorData.message });

      }
    } catch (error) {
      console.error('Error al realizar la solicitud de registro:', error);
    }
  };



  return (
    <div className="login-form">
     

      <div className={`wrapper${action}`}>
        <div className="form-box login">
          <form action="" onSubmit={loginEP}>
            <h1>Iniciar sesion</h1>
            {alert.message && (
                    <Alert severity={alert.severity}>{alert.message}</Alert>
            )}
            <div className="input-box">
              <input type="text" name="sobrenom" placeholder='Sobrenom' required />
              <FaUserAstronaut  className='icono'/>
            </div>
            <div className="input-box">
              <input type={passwordVisible ? 'text' : 'password'} name="contrasenya" placeholder='Contraseña' required />
              <RiLockPasswordFill  className='icono'/>
              {passwordVisible ? <IoIosEye className='showPass' onClick={togglePasswordVisibility}/>
              : <IoIosEyeOff className='showPass' onClick={togglePasswordVisibility}/>}
            </div>
            <div className="recordar-olvidada">
              <label><input type="checkbox" />Recordar contraseña</label>
              <a href="#">Contraseña olvidada?</a>
            </div>
            <button type='submit'>Login</button>
                  {/* Alerta de error */}

            <div className="registro-link">
              <p>¿No tienes cuenta? <a href="#" onClick={registrarse}>Crear cuenta</a></p>
            </div>
          </form>
        </div>


        <div className="form-box registro">
          <form action="" onSubmit={registrarseEP}>
            <h1>Registro</h1>
            <div className="input-box">
            <input type="text" name="nom" placeholder='Nom' required />
              <FaUserAlt  className='icono'/>
            </div>
            <div className="input-box">
              <input type="email" name="email" placeholder='Email' required />
              <IoMdMail  className='icono'/>
            </div>
            <div className="input-box">
            <input type={passwordVisible ? 'text' : 'password'} name="contrasenya" placeholder='Contraseña' required />
              <RiLockPasswordFill  className='icono'/>
              {passwordVisible ? <IoIosEye className='showPass' onClick={togglePasswordVisibility}/>
              : <IoIosEyeOff className='showPass' onClick={togglePasswordVisibility}/>}
            </div>
            <div className="input-box">
              <input type="text" name="sobrenom" placeholder='Sobrenom' required />
              <FaUserAstronaut  className='icono'/>
            </div>

            <div className="input-box">
              <input type="date" name="datanaixement" placeholder='Data de naixement' required />
              <FaUserAstronaut  className='icono'/>
            </div>

            <button type='submit'>Registrarse</button>

            <div className="registro-link">
              <p>Ya tienes cuenta? <a href="#"onClick={login}>Inicia sesion</a></p>
            </div>
          </form>
        </div>
      </div>

    </div>
  );
};

export default LoginRegistro