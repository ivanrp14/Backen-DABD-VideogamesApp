import React, {useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Box from '@mui/material/Box';
import SidenavUsuari from "../../Componentes/Sidenav/UsuariSidenav";
import Navbar from '../../Componentes/NavBar';
const BASE_URL = 'http://localhost:8000';

const Usuarios = () => {
  const [rows, setRows] = useState([])
  const eliminarUsuari = async (sobrenom) => {
  try {
    const token = JSON.parse(localStorage.getItem("token"));
    const accessToken = token?.access_token;
    if (!accessToken) throw new Error("No hay token de acceso");

    const response = await fetch(`http://localhost:8000/usuaris/${sobrenom}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      }
    });

    if (!response.ok) throw new Error("Error al eliminar el usuario");

    console.log(`Usuario ${sobrenom} eliminado correctamente`);
    return true;
  } catch (error) {
    console.error(error);
    return false;
  }
};

  const columns = [
    {
      field: 'sobrenom',
      headerName: 'Username',
      width: 200,
      editable: false
    },
    {
      field: 'Nom',
      headerName: 'Nombre',
      width: 200,
      editable: false
    },
    {
      field: 'correuelectronic',
      headerName: 'Correo electronico',
      width: 200,
      editable: false
    },
    {
      field: 'datanaixement',
      headerName: 'Fecha de nacimiento',
      width: 150,
      editable: false
    },{
  field: 'acciones',
  headerName: 'Acciones',
  width: 150,
  renderCell: (params) => (
    <button
      onClick={async () => {
        const confirmado = window.confirm(`¿Eliminar a ${params.row.sobrenom}?`);
        if (confirmado) {
          const exito = await eliminarUsuari(params.row.sobrenom);
          if (exito) {
            setRows((prev) => prev.filter(row => row.sobrenom !== params.row.sobrenom));
          }
        }
      }}
      style={{ backgroundColor: 'red', color: 'white', border: 'none', padding: '5px 10px', cursor: 'pointer' }}
    >
      Eliminar
    </button>
  )
}

  ];
  useEffect(() => {
    const getUsuarios = async (event) => {
      try {
        const accessToken = localStorage.getItem("token");
        const sobrenom = localStorage.getItem("sobrenom");

        const response = await fetch(`${BASE_URL}/vendes/usuari/${sobrenom}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${accessToken}`
          }
        })

      if (!response.ok) {
        throw new Error("Error al obtener los usuarios");
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

    getUsuarios();
}, []);
  return (
    <>
    <Navbar/>
    <Box height={40}/>
    <Box sx={{  display: 'flex'}}>
      <SidenavUsuari/>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <h1>Usuarios</h1>
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

export default Usuarios;