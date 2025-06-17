import React, { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button } from '@mui/material';
import Box from '@mui/material/Box';
import SidenavUsuari from "../../Componentes/Sidenav/UsuariSidenav";
import Navbar from '../../Componentes/NavBar';

const BASE_URL = 'http://localhost:8000';

const Videojocs = () => {
  const [rows, setRows] = useState([]);

  const comprarVideojoc = async (videojocId) => {
    try {
      const accessToken = localStorage.getItem("token");
      const sobrenom = localStorage.getItem("sobrenom");
      if (!accessToken) {
        alert("Debes iniciar sesión para comprar.");
        return;
      }

      const response = await fetch(`${BASE_URL}/vendes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
          usuarisobrenom:sobrenom,
          elementvendaid:videojocId
        })
      });

      if (!response.ok) throw new Error("Error al realizar la compra");

      alert("¡Producto comprado con éxito!");
    } catch (error) {
      console.error("Error al comprar:", error);
      alert("Hubo un error al realizar la compra.");
    }
  };


  const columns = [
    { field: 'nom', headerName: 'Nombre', width: 200 },
    { field: 'descripcio', headerName: 'Descripcion', width: 200 },
    { field: 'preu', headerName: 'Precio', width: 150 },
    { field: 'datallancament', headerName: 'Fecha de lanzamiento', width: 250 },
    { field: 'qualificacioedat', headerName: 'Qualificacion por edat', width: 150 },
    { field: 'desenvolupador', headerName: 'Desarrollador', width: 200 },
    { field: 'tipus', headerName: 'tipus', width: 200 },
    {
      field: 'acciones',
      headerName: '',
      width: 150,
      renderCell: (params) => (
        <Button
          variant="contained"
          color="primary"
          onClick={() => comprarVideojoc(params.row.id)}
        >
          Comprar
        </Button>
      )
    }
  ];

  useEffect(() => {
    const getVideojocs = async () => {
      try {
        const accessToken = localStorage.getItem("token");
        const response = await fetch(`${BASE_URL}/products/by-date`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${accessToken}`
          }
        });

        if (!response.ok) {
          throw new Error("Error al obtener los videojuegos");
        }

        const data = await response.json();
        const rowsConId = data.products.map((item, index) => ({ id: item.id || index, ...item }));
        setRows(rowsConId);

      } catch (error) {
        console.error(error);
      }
    };

    getVideojocs();
  }, []);

  return (
    <>
      <Navbar />
      <Box height={40} />
      <Box sx={{ display: 'flex' }}>
        <SidenavUsuari />
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <h1>Tienda</h1>
          <Box height={75} />
          <Box sx={{ Width: '80vw', margin: '0 auto', width: '100%' }}>
            <div style={{ height: '100%', width: '100%', minHeight: '100px' }}>
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
  );
};

export default Videojocs;
