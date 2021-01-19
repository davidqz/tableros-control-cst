class Cliente {
  String nombre;
  String sector;
  String pais;
  String estado;
  String ciudad;

  Cliente(this.nombre, this.sector, this.pais, this.estado, this.ciudad);

  Cliente.fromJson(Map<String, dynamic> json)
      : nombre = json['nombre'],
        sector = json['sector'],
        pais = json['pais'],
        estado = json['estado'],
        ciudad = json['ciudad'];
}

class Avance {
  int mes;
  int anyo;
  int porcentajeAvance;

  Avance(this.mes, this.anyo, this.porcentajeAvance);

  Avance.fromJson(Map<String, dynamic> json)
      : mes = json['mes'],
        anyo = json['anyo'],
        porcentajeAvance = json['porcentajeAvance'];
}

class Servicio {
  String idServicio;
  String interno;
  String nombreCorto;
  String areaResponsable;
  String estatus;
  String alcance;
  Cliente cliente;
  String fechaInicioProgramada;
  String fechaFinProgramada;
  List<Avance> avances;

  Servicio(
      this.idServicio,
      this.interno,
      this.nombreCorto,
      this.areaResponsable,
      this.estatus,
      this.alcance,
      this.cliente,
      this.fechaFinProgramada,
      this.fechaInicioProgramada,
      this.avances);

  Servicio.fromJson(Map<String, dynamic> json)
      : idServicio = json['idServicio'],
        interno = json['interno'],
        nombreCorto = json['nombreCorto'],
        areaResponsable = json['areaResponsable'],
        estatus = json['estatus'],
        alcance = json['alcance'],
        cliente = Cliente.fromJson(json['cliente']),
        fechaInicioProgramada = json['fechaInicioProgramada'],
        fechaFinProgramada = json['fechaFinProgramada'] {
    // print('------ Servicio.fromJson()');
    avances = (json['avances'] as List)
        .map<Avance>((json) => Avance.fromJson(json))
        .toList();
  }
}
