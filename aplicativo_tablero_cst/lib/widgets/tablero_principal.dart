import 'package:aplicativo_tablero_cst/utilidades/modelo_datos.dart';
import 'package:aplicativo_tablero_cst/widgets/indicador_texto.dart';
import 'package:flutter/material.dart';

class TableroPrincipal extends StatelessWidget {
  TableroPrincipal({@required this.servicios}) {
    _serviciosInternos = servicios.where((s) => s.interno == '1').length;
    _serviciosAbiertos = servicios.where((s) => s.estatus == 'Abierto').length;
  }

  final List<Servicio> servicios;
  int _serviciosInternos = 0;
  int _serviciosAbiertos = 0;
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 0),
      child: Card(
        margin: EdgeInsets.zero,
        color: Colors.grey[100],
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  IndicadorTexto(
                    titulo: 'Total servicios',
                    valor: '${servicios.length}',
                  ),
                  IndicadorTexto(
                    titulo: 'Servicios Internos',
                    valor: '${_serviciosInternos}',
                  ),
                  IndicadorTexto(
                    titulo: 'Servicios Abiertos',
                    valor: '${_serviciosAbiertos}',
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
