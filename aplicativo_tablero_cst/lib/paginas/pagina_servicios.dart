import 'dart:convert';

import 'package:aplicativo_tablero_cst/utilidades/constantes.dart';
import 'package:aplicativo_tablero_cst/utilidades/modelo_datos.dart';
import 'package:aplicativo_tablero_cst/widgets/tablero_principal.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:flutter/widgets.dart';

class PaginaServicios extends StatelessWidget {
  Future<List<Servicio>> obtenerDatos() async {
    print("obtenerDatos");
    String jsonStr =
        await rootBundle.loadString("datos/serviciosDesarrollo.json");
    return compute(procesarJson, jsonStr);
  }

  List<Servicio> procesarJson(String jsonStr) {
    print("procesarJson");
    final data = json.decode(jsonStr)["servicios"] as List;
    return data.map<Servicio>((json) => Servicio.fromJson(json)).toList();
  }

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
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Card(
                  margin: EdgeInsets.zero,
                  color: kColorPrimario,
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                        vertical: 8.0, horizontal: 32.0),
                    child: Text('Servicios',
                        style: Theme.of(context)
                            .textTheme
                            .headline6
                            .apply(color: Colors.white)),
                  ),
                ),
                Card(
                  margin: EdgeInsets.zero,
                  color: kColorPrimario,
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                        vertical: 8.0, horizontal: 32.0),
                    child: Text('2019',
                        style: Theme.of(context)
                            .textTheme
                            .headline6
                            .apply(color: Colors.white)),
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: FutureBuilder<List<Servicio>>(
              future: obtenerDatos(),
              builder: (context, snapshot) {
                if (snapshot.hasError) print(snapshot.error);
                return snapshot.hasData
                    ? TableroPrincipal(servicios: snapshot.data)
                    : Padding(
                        padding: const EdgeInsets.only(top: 32),
                        child: Center(child: CircularProgressIndicator()),
                      );
              },
            ),
          ),
        ],
      ),
    );
  }
}
