import React, {useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Box from '@mui/material/Box';
import SidenavUsuari from "../../Componentes/Sidenav/UsuariSidenav";
import Navbar from '../../Componentes/NavBar';
import { data } from 'react-router-dom';
const BASE_URL = 'http://localhost:8000';

const MiSubscripcio = () => {
  const [rows, setRows] = useState([])
  const columns = [
    {
      field: 'Nom',
      headerName: 'Nombre',
      width: 200,
      editable: false
    },
    {
      field: 'Descripcio',
      headerName: 'Descripcion',
      width: 200,
      editable: false
    },
    {
      field: 'preu',
      headerName: 'Precio',
      width: 150,
      editable: false
    },
    {
      field: 'data',
      headerName: 'Fecha de lanzamiento',
      width: 250,
      editable: false
    },
    {
      field: 'edat',
      headerName: 'Qualificacion por edat',
      width: 150,
      editable: false
    },
    {
      field: 'desenvolupador',
      headerName: 'Desarrollador',
      width: 370,
      editable: false
    }
  ];
  


  useEffect(() => {
    const getSubscripcionsUsuari = async (event) => {
  try {
    const token = localStorage.getItem("token");
    const sobrenom = localStorage.getItem("sobrenom");
    if (!token) {
      throw new Error("No hay token de acceso, inicia sesión.");
    }

    const response = await fetch(`${BASE_URL}/vendes/usuari/${sobrenom}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error("Error al obtener las suscripciones");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
};
    const getVideojocs = async (event) => {
      try {
        const accessToken = localStorage.getItem("token");
        const sobrenom = localStorage.getItem("sobrenom");
        const id = data.id;
        const response = await fetch(`${BASE_URL}/subscripcions/subscripcions/${id}/jocs`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${accessToken}`
          }
        })

      if (!response.ok) {
        throw new Error("Error al obtener los videojuegos");
      }

      const data = await response.json();
      console.log(data);
      
      // Si los objetos no tienen `id`, puedes generarlo temporalmente:
      const rowsConId = data.map((item, index) => ({ id: index, ...item }));
      setRows(rowsConId);

    } catch (error) {
      console.error(error);
    }
  };
  
  getSubscripcionsUsuari();
  getVideojocs();

}, []);
  return (
    <>
    <Navbar/>
    <Box height={40}/>
    <Box sx={{  display: 'flex'}}>
      <SidenavUsuari/>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <h1>Mi subscripcion</h1>
        <div className="subscripcio-container">
              <p><strong>Tipo:</strong> {data.nom}</p>
              <p><strong>Fecha de inicio:</strong> {data.datainici}</p>
              <p><strong>Fecha de fin:</strong> {data.datafi}</p>
        </div>
        <Box height={75}/>
          <Box sx={{ maxWidth: '80vw', margin: '0 auto', alignItems: 'center', width: '60%'}}>
            <div style={{ height: '100%', width: '100%', minHeight:'100px' }}>
              <DataGrid
                rows={rows}
                columns={columns}
                getRowId={(row) => row.id}
                pageSize={10}
                disableRowSelectionOnClick
                isCellEditable={() => false}
              />
            </div>
          </Box>
        </Box>
      </Box>
    </>
  )
}

export default MiSubscripcio;
