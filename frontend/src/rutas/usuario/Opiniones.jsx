import React, { useEffect, useState } from 'react';
import { Box, Typography, Rating, Button } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import Navbar from '../../Componentes/NavBar';
import Sidenav from '../../Componentes/Sidenav/UsuariSidenav';

const BASE_URL = 'http://localhost:8000';

const OpinionsUsuari = () => {
  const [opinions, setOpinions] = useState([]);

  const fetchOpinions = async () => {
    const accessToken = localStorage.getItem("token");
    const sobrenom = localStorage.getItem("sobrenom");

    try {
      const response = await fetch(`${BASE_URL}/opinions/user/${sobrenom}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        }
      });

      if (!response.ok) throw new Error("Error al obtener las reseñas");

      const data = await response.json();

      const rowsConId = data.map((item) => ({
        id: item.id,
        opinion: item.textopinio,
        puntuacio: item.puntuacio,
        videojocId: item.elementvendaid,
        data: item.datapublicacio,
        usuari: item.usuarisobrenom
      }));

      setOpinions(rowsConId);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchOpinions();
  }, []);

  const handleDeleteOpinion = async (id) => {
    const accessToken = localStorage.getItem("token");

    if (!window.confirm("¿Estás seguro de que quieres eliminar esta reseña?")) return;

    try {
      const response = await fetch(`${BASE_URL}/opinions/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      if (!response.ok) throw new Error("Error al eliminar la reseña");

      // Actualizar el estado quitando la opinión eliminada
      setOpinions((prev) => prev.filter((op) => op.id !== id));
    } catch (error) {
      console.error(error);
      alert("No se pudo eliminar la opinión");
    }
  };

  const columns = [
    { field: 'videojocId', headerName: 'ID del videojoc', width: 150 },
    { field: 'opinion', headerName: 'Opinión', width: 300 },
    {
      field: 'puntuacio',
      headerName: 'Valoración',
      width: 150,
      renderCell: (params) => (
        <Rating value={params.value} readOnly />
      )
    },
    { field: 'data', headerName: 'Fecha', width: 150 },
    { field: 'usuari', headerName: 'Usuario', width: 150 },
    {
      field: 'acciones',
      headerName: 'Acciones',
      width: 150,
      renderCell: (params) => (
        <Button
          variant="outlined"
          color="error"
          size="small"
          onClick={() => handleDeleteOpinion(params.row.id)}
        >
          Eliminar
        </Button>
      )
    }
  ];

  return (
    <Box sx={{ width: '70%', margin: 'auto', mt: 4 }}>
      <Sidenav/>
      <Navbar/>
      <Typography variant="h4" gutterBottom>
        Reseñas del usuario
      </Typography>
      <div style={{ height: 400, width: '100%' }}>
        <DataGrid
          rows={opinions}
          columns={columns}
          pageSize={5}
          disableRowSelectionOnClick
        />
      </div>
    </Box>
  );
};

export default OpinionsUsuari;


