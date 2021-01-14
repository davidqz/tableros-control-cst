import 'package:aplicativo_tablero_cst/constantes.dart';
import 'package:flutter/material.dart';

class FormularioIngreso extends StatefulWidget {
  FormularioIngreso({Key key}) : super(key: key);

  @override
  _FormularioIngresoState createState() => _FormularioIngresoState();
}

class _FormularioIngresoState extends State<FormularioIngreso> {
  final _controladorTextoUsuario = TextEditingController();
  final _controladorTextoContrasena = TextEditingController();

  void _autenticarUsuario() {
    print(_controladorTextoUsuario.text);
    print(_controladorTextoContrasena.text);

    Navigator.of(context).pushNamed('/servicios');
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Padding(
            padding: EdgeInsets.all(8.0),
            child: TextFormField(
              controller: _controladorTextoUsuario,
              decoration: InputDecoration(
                  hintText: 'Usuario', border: OutlineInputBorder()),
            ),
          ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: TextFormField(
              obscureText: true,
              onFieldSubmitted: (_) => _autenticarUsuario(),
              controller: _controladorTextoContrasena,
              decoration: InputDecoration(
                  hintText: 'Contraseña', border: OutlineInputBorder()),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: RaisedButton(
              textColor: Colors.white,
              color: kColorSecundario,
              child: Text('Ingresar'),
              padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
              onPressed: _autenticarUsuario,
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _controladorTextoUsuario.dispose();
    super.dispose();
  }
}
