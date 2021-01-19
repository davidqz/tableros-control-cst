import 'package:aplicativo_tablero_cst/utilidades/constantes.dart';
import 'package:aplicativo_tablero_cst/widgets/formulario_ingreso.dart';
import 'package:flutter/material.dart';

class PaginaInicioSesion extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).backgroundColor,
      body: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Padding(
                padding: const EdgeInsets.all(24.0),
                child: Image(
                  image: AssetImage('imagenes/logo_conacyt.png'),
                  height: 80,
                ),
              ),
              Text('Coordinación de Servicios Tecnológicos',
                  style: Theme.of(context)
                      .textTheme
                      .headline3
                      .apply(color: kColorPrimario)),
              Padding(
                padding: const EdgeInsets.all(24.0),
                child: Image(
                  image: AssetImage('imagenes/logo_cimat.png'),
                  height: 80,
                ),
              ),
            ],
          ),
          SizedBox(height: 50),
          SizedBox(
            width: 400,
            child: Card(
              color: Colors.grey[100],
              child: Padding(
                padding: const EdgeInsets.all(32.0),
                child: FormularioIngreso(),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
