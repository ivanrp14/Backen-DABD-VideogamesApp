import React, {useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Box from '@mui/material/Box';
import SidenavUsuari from "../../Componentes/Sidenav/UsuariSidenav";
import Navbar from '../../Componentes/NavBar';
const BASE_URL = 'http://localhost:8000';

const Videojocs = () => {
  const [rows, setRows] = useState([])
  const columns = [
    {
      field: 'Nom',
      headerName: 'Nom',
      width: 200,
      editable: false
    },
    {
      field: 'Descripcio',
      headerName: 'Descripcio',
      width: 200,
      editable: false
    },
    {
      field: 'Preu',
      headerName: 'Preu',
      width: 150,
      editable: false
    },
    {
      field: 'data_Ll',
      headerName: 'Data de llançament',
      width: 250,
      editable: false
    },
    {
      field: 'edat',
      headerName: 'Qualificacio edat',
      width: 150,
      editable: false
    },
    {
      field: 'desenvolupador',
      headerName: 'desenvolupador',
      width: 370,
      editable: false
    }
  ];
  useEffect(() => {
    const getVideojocs = async (event) => {
      try {
        const token = JSON.parse(localStorage.getItem("token"));
        const accessToken = token.access_token;
        const response = await fetch(`${BASE_URL}/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${accessToken}`
          }
        })
        if (response.ok) {
          const data = await response.json()
          console.log(data)
          setRows(data)
        }
      } catch (error) {
        console.error(error)
      }
    }
    getVideojocs()
    // return () => rows
  }, [])
  return (
    <>
    <Navbar/>
    <Box height={40}/>
    <Box sx={{  display: 'flex'}}>
      <SidenavUsuari/>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <h1>Biblioteca</h1>
        <Box height={75}/>
          <Box sx={{ maxWidth: '80vw', margin: '0 auto', alignItems: 'center', width: '60%'}}>
            <div style={{ height: '100%', width: '100%', minHeight:'100px' }}>
              <DataGrid
                rows={rows}
                columns={columns}
                getRowId={(row) => row.username}
                rowsPerPageOptions={[10]}
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

export default Videojocs;