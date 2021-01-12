import 'package:aplicativo_tablero_cst/constants.dart';
import 'package:flutter/material.dart';

class SignUpScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).backgroundColor,
      body: Row(
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
    );
  }
}
