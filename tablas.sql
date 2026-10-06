CREATE TABLE usuarios (
 id INT AUTO_INCREMENT PRIMARY KEY,
 nombre VARCHAR(80) NOT NULL,
 correo VARCHAR(120) NOT NULL UNIQUE,
 departamento VARCHAR(80) NOT NULL,
 creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE perfiles_usuario (
 id INT AUTO_INCREMENT PRIMARY KEY,
 usuario_id INT NOT NULL UNIQUE,
 telefono VARCHAR(20),
 ubicacion VARCHAR(80),
 FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE tecnicos (
 id INT AUTO_INCREMENT PRIMARY KEY,
 nombre VARCHAR(80) NOT NULL,
 correo VARCHAR(120) NOT NULL UNIQUE,
 activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE especialidades (
 id INT AUTO_INCREMENT PRIMARY KEY,
 nombre VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE tecnico_especialidad (
 tecnico_id INT NOT NULL,
 especialidad_id INT NOT NULL,
 PRIMARY KEY (tecnico_id, especialidad_id),
 FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id) ON DELETE CASCADE,
 FOREIGN KEY (especialidad_id) REFERENCES especialidades(id) ON DELETE CASCADE
);

CREATE TABLE tickets (
 id INT AUTO_INCREMENT PRIMARY KEY,
 usuario_id INT NOT NULL,
 tecnico_id INT NULL,
 titulo VARCHAR(120) NOT NULL,
 descripcion TEXT NOT NULL,
 prioridad ENUM('Baja','Media','Alta') NOT NULL DEFAULT 'Media',
 estado ENUM('Abierto','En proceso','Resuelto') NOT NULL DEFAULT 'Abierto',
 creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
 FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id) ON DELETE SET NULL
);

CREATE TABLE historial_tickets (
 id INT AUTO_INCREMENT PRIMARY KEY,
 ticket_id INT NOT NULL,
 estado_anterior VARCHAR(30) NOT NULL,
 estado_nuevo VARCHAR(30) NOT NULL,
 fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE
);

INSERT INTO especialidades(nombre) VALUES ('Hardware'),('Software'),('Redes');
INSERT INTO usuarios(nombre,correo,departamento) VALUES ('Ana Soto','ana@demo.cl','Administración'),('Luis Pérez','luis@demo.cl','Ventas');
INSERT INTO perfiles_usuario(usuario_id,telefono,ubicacion) VALUES (1,'912345678','Oficina 1'),(2,'923456789','Oficina 2');
INSERT INTO tecnicos(nombre,correo) VALUES ('Camila Rojas','camila@demo.cl'),('Diego Mora','diego@demo.cl');
INSERT INTO tecnico_especialidad VALUES (1,1),(1,2),(2,3),(2,2);
INSERT INTO tickets(usuario_id,tecnico_id,titulo,descripcion,prioridad,estado) VALUES
(1,1,'PC no inicia','El equipo no inicia Windows','Alta','Abierto'),
(2,2,'Sin acceso a red','No hay conexión en el puesto','Media','En proceso');
