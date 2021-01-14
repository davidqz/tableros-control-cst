import 'package:flutter/material.dart';

import '../constantes.dart';

class PaginaServicios extends StatefulWidget {
  PaginaServicios({Key key}) : super(key: key);

  @override
  _PaginaServiciosState createState() => _PaginaServiciosState();
}

class _PaginaServiciosState extends State<PaginaServicios> {
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
                  image: AssetImage('images/logo_conacyt.png'),
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
                  image: AssetImage('images/logo_cimat.png'),
                  height: 80,
                ),
              ),
            ],
          ),
          SizedBox(height: 50),
        ],
      ),
    );
  }
}
