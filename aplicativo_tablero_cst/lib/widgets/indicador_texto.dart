import 'package:flutter/material.dart';

class IndicadorTexto extends StatelessWidget {
  IndicadorTexto({@required this.titulo, @required this.valor});

  final String titulo;
  final String valor;
  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(titulo, style: Theme.of(context).textTheme.bodyText2),
            SizedBox(
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Text(
                    valor,
                    style: Theme.of(context).textTheme.headline5,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
