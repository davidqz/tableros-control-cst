import 'package:aplicativo_tablero_cst/constantes.dart';
import 'package:aplicativo_tablero_cst/paginas/pagina_inicio_sesion.dart';
import 'package:aplicativo_tablero_cst/paginas/pagina_servicios.dart';
import 'package:flutter/material.dart';

void main() => runApp(MainApp());

class MainApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      routes: {
        '/': (context) => PaginaInicioSesion(),
        '/servicios': (context) => PaginaServicios(),
      },
      title: 'Tablero de Indicadores CST',
      theme: ThemeData(
          primaryColor: kColorPrimario,
          accentColor: kColorSecundario,
          backgroundColor: kColorFondo),
    );
  }
}
