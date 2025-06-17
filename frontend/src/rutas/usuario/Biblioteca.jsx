import React, { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import {
  Box, Button, Dialog, DialogActions,
  DialogContent, DialogTitle, TextField, Rating, Typography
} from '@mui/material';
import SidenavUsuari from "../../Componentes/Sidenav/UsuariSidenav";
import Navbar from '../../Componentes/NavBar';

const BASE_URL = 'http://localhost:8000';

const Videojocs = () => {
  const [rows, setRows] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedJoc, setSelectedJoc] = useState(null);
  const [opinionText, setOpinionText] = useState('');
  const [valoracio, setValoracio] = useState(0);

const columns = [
  { field: 'nom', headerName: 'Nombre', width: 200 },
  { field: 'descripcio', headerName: 'Descripción', width: 200 },
  { field: 'preu', headerName: 'Precio', width: 150 },
  { field: 'datallancament', headerName: 'Fecha de lanzamiento', width: 250 },
  { field: 'qualificacioedat', headerName: 'Calificación por edad', width: 150 },
  { field: 'desenvolupador', headerName: 'Desarrollador', width: 250 },
  { field: 'tipus', headerName: 'Tipo', width: 250 },
  {
    field: 'accion',
    headerName: 'Acción',
    width: 150,
    renderCell: (params) => (
      <Button
        variant="outlined"
        size="small"
        onClick={() => handleOpenDialog(params.row)}
      >
        Opinar
      </Button>
    )
  }
];


  useEffect(() => {
    const getVideojocs = async () => {
      try {
        const accessToken = localStorage.getItem("token");
        const usuarisobrenom = localStorage.getItem("sobrenom");

        const response = await fetch(`${BASE_URL}/products/user/${usuarisobrenom}/accessos`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
          }
        });

        if (!response.ok) throw new Error("Error al obtener los videojuegos");

        const data = await response.json();
        const rowsConId = data.products.map((item, index) => ({ id: index, ...item }));
        setRows(rowsConId);

      } catch (error) {
        console.error(error);
      }
    };

    getVideojocs();
  }, []);

  const handleOpenDialog = (joc) => {
    setSelectedJoc(joc);
    setOpinionText('');
    setValoracio(0);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedJoc(null);
  };

  const enviarOpinion = async () => {
    const accessToken = localStorage.getItem("token");
    const sobrenom = localStorage.getItem("sobrenom");

    if (!opinionText || !valoracio) {
      alert("Debes escribir una opinión y una valoración.");
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/opinions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
          usuarisobrenom: sobrenom,
          elementvendaid: selectedJoc.id,
          textopinio: opinionText,
          puntuacio: valoracio
        })
      });

      if (!response.ok) throw new Error("Error al enviar la opinión");
      alert("Opinión enviada correctamente");
      handleCloseDialog();
    } catch (error) {
      console.error(error);
      alert("Error al enviar la opinión");
    }
  };

  return (
    <>
      <Navbar />
      <Box height={40} />
      <Box sx={{ display: 'flex' }}>
        <SidenavUsuari />
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <h1>Biblioteca</h1>
          <Box height={75} />
          <Box sx={{ maxWidth: '90vw', margin: '0 auto', width: '100%' }}>
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

      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>Escribe tu opinión sobre {selectedJoc?.nom}</DialogTitle>
        <DialogContent>
          <TextField
            label="Opinión"
            multiline
            rows={4}
            fullWidth
            value={opinionText}
            onChange={(e) => setOpinionText(e.target.value)}
            sx={{ mt: 2 }}
          />
          <Box sx={{ mt: 2 }}>
            <Typography component="legend">Valoración</Typography>
            <Rating
              name="valoracion"
              value={valoracio}
              onChange={(event, newValue) => setValoracio(newValue)}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancelar</Button>
          <Button variant="contained" onClick={enviarOpinion}>Enviar</Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default Videojocs;
