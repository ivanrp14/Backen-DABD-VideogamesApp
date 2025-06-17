import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Sidenav from '../../Componentes/Sidenav/UsuariSidenav';
import './perfil.css'
import {AiOutlineMail, AiOutlinePhone} from 'react-icons/ai'
import Navbar from '../../Componentes/NavBar';
import { AiOutlineCalendar } from 'react-icons/ai';

export default function MiPerfil() {
  const BASE_URL = 'http://localhost:8000';
  const [username, setUsername] = useState('');
  const [nombre, setNombre] = useState('');
  const [contrasenya, setContrasenya] = useState('');
  const [datanaixement, setdataNaixement] = useState('');
  const [email, setEmail] = useState('');

  useEffect(() => {
    const getPerfil = async () => {
      const accessToken = localStorage.getItem("token");
      console.log(accessToken);
      try {
        const response = await fetch(`${BASE_URL}/auth/get-user`, {
          method: 'GET',
          headers: {
            "Authorization": `Bearer ${accessToken}`
          },
        });

        if (!response.ok) {
          throw new Error('No se pudo obtener informacion');
        }
        const data = await response.json();
        console.log(data)
        setUsername(data.sobrenom)
        setNombre(data.nom)
        setContrasenya(data.contrasenya)
        setdataNaixement(data.datanaixement)
        setEmail(data.correuelectronic)
      } catch (error) {
        console.error('Error al obtener mi perfil:', error);
      }
    };

    getPerfil();
  }, []);

  return (
    <>
      <Navbar />
      <Box height={40} />
      <Box sx={{ display: 'flex' }}>
        <Sidenav/>
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <h1>Mi perfil</h1>
          <div className="perfil-container">
            <div className="perfil-box">
              <img width="100px" src="https://robohash.org/propietario"></img>
              <div>
                <h3>Username:@{username} </h3>
                <p className="perfil-nombre">Nombre: {nombre}</p>
                <p><AiOutlineCalendar /> Fecha de nacimiento: {new Date(datanaixement).toLocaleDateString()}</p>
                <p><AiOutlineMail/> {email}</p>
                
              </div>
            </div>
          </div>
        </Box>
      </Box>
    </>
  );
}