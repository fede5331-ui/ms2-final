CREATE DATABASE IF NOT EXISTS ayuda_animal
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ayuda_animal;

CREATE TABLE usuarios (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  nombre        VARCHAR(100) NOT NULL,
  email         VARCHAR(150) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  rol           ENUM('comunidad','moderador') NOT NULL DEFAULT 'comunidad',
  creado_en     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pedidos (
  id              INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id      INT NOT NULL,
  titulo          VARCHAR(150) NOT NULL,
  descripcion     TEXT NOT NULL,
  monto_objetivo  DECIMAL(10,2) NOT NULL CHECK (monto_objetivo > 0),
  monto_recaudado DECIMAL(10,2) NOT NULL DEFAULT 0,
  estado          ENUM('abierto','cerrado') NOT NULL DEFAULT 'abierto',
  rendicion       TEXT NULL,
  cerrado_en      DATETIME NULL,
  creado_en       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_pedidos_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE aportes (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  pedido_id  INT NOT NULL,
  usuario_id INT NOT NULL,
  monto      DECIMAL(10,2) NOT NULL CHECK (monto > 0),
  creado_en  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_aportes_pedido  FOREIGN KEY (pedido_id)  REFERENCES pedidos(id),
  CONSTRAINT fk_aportes_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE novedades (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  pedido_id  INT NOT NULL,
  usuario_id INT NOT NULL,
  texto      TEXT NOT NULL,
  creado_en  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_novedades_pedido  FOREIGN KEY (pedido_id)  REFERENCES pedidos(id),
  CONSTRAINT fk_novedades_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

DELIMITER $$

CREATE PROCEDURE sp_registrar_aporte(
  IN p_pedido_id  INT,
  IN p_usuario_id INT,
  IN p_monto      DECIMAL(10,2)
)
BEGIN
  DECLARE v_estado VARCHAR(10);

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    ROLLBACK;
    RESIGNAL;
  END;

  START TRANSACTION;

  SELECT estado INTO v_estado
  FROM pedidos
  WHERE id = p_pedido_id
  FOR UPDATE;

  IF v_estado IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El pedido no existe';
  END IF;

  IF v_estado = 'cerrado' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El pedido ya está cerrado';
  END IF;

  INSERT INTO aportes (pedido_id, usuario_id, monto)
  VALUES (p_pedido_id, p_usuario_id, p_monto);

  UPDATE pedidos
  SET monto_recaudado = monto_recaudado + p_monto
  WHERE id = p_pedido_id;

  COMMIT;
END$$

DELIMITER ;