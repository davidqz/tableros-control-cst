import 'package:aplicativo_tablero_cst/constants.dart';
import 'package:aplicativo_tablero_cst/screens/sign_up_screen.dart';
import 'package:flutter/material.dart';

void main() => runApp(MainApp());

class MainApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      routes: {
        '/': (context) => SignUpScreen(),
      },
      title: 'Tablero CST',
      theme: ThemeData(
          primaryColor: kColorPrimario,
          accentColor: kColorSecundario,
          backgroundColor: kColorFondo),
    );
  }
}
