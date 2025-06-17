import './MenuPrincipal.css'
import Inicio from '../../rutas/usuario/Biblioteca'
import Perfil from '../../rutas/usuario/perfil'
import Subscripcion from '../../rutas/usuario/MiSubscripcion'
import Videojuegos from'../../rutas/usuario/Videojuegos'
import Usuarios  from '../../rutas/Administracion/Usuarios'
import Opiniones from '../../rutas/usuario/Opiniones'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import LoginRegistro from '../Login/LoginRegistro'

const MenuPrincipal = () =>{
return(
    <Router>
        <Routes>
            <Route>
                <Route path='/Inicio' element = {<Inicio/>}/>
                <Route path='/Perfil' element= {<Perfil/>}/>
                <Route path='/MiSubscripcion' element= {<Subscripcion/>}/>
                <Route path='/Comprar' element= {<Videojuegos/>}/>
                <Route path='/Admin/Usuarios' element= {<Usuarios/>}/>
                <Route path='/Opinion' element= {<Opiniones/>}/>
            </Route>    
        <Route path='/' element = {<LoginRegistro/>}/>    
        </Routes>
        
    </Router>
);

};

export default MenuPrincipal;