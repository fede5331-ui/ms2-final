-- sql/datos_prueba.sql
-- Datos de ejemplo para probar la API y el frontend.
-- EJECUTAR UNA SOLA VEZ: si se corre dos veces, falla porque los
-- emails de los usuarios son únicos (UNIQUE) y no se pueden repetir.
-- Todos los usuarios tienen la contraseña: Prueba123

USE ayuda_animal;

-- ---------------------------------------------------------------
-- 1) USUARIOS
-- El password_hash es el bcrypt de "Prueba123" (nunca se guarda
-- la contraseña en texto plano). Un solo hash sirve para los cuatro.
-- El primero tiene rol 'moderador'; los demás, 'comunidad'.
-- ---------------------------------------------------------------
INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES
('Admin Moderador', 'moderador@ayudaanimal.com', '$2b$12$22s2e/65B01xGOU32iBZGe6EldLB2uAZRMjbid2DyefWv.4VE7c3u', 'moderador'),
('Lucía Fernández', 'lucia@ejemplo.com',        '$2b$12$22s2e/65B01xGOU32iBZGe6EldLB2uAZRMjbid2DyefWv.4VE7c3u', 'comunidad'),
('Martín Gómez',    'martin@ejemplo.com',       '$2b$12$22s2e/65B01xGOU32iBZGe6EldLB2uAZRMjbid2DyefWv.4VE7c3u', 'comunidad'),
('Carla Díaz',      'carla@ejemplo.com',        '$2b$12$22s2e/65B01xGOU32iBZGe6EldLB2uAZRMjbid2DyefWv.4VE7c3u', 'comunidad');

-- Guardamos los ids de los usuarios en variables (@nombre) para
-- usarlos abajo sin tener que saber qué número les tocó.
SET @mod    = (SELECT id FROM usuarios WHERE email = 'moderador@ayudaanimal.com');
SET @lucia  = (SELECT id FROM usuarios WHERE email = 'lucia@ejemplo.com');
SET @martin = (SELECT id FROM usuarios WHERE email = 'martin@ejemplo.com');
SET @carla  = (SELECT id FROM usuarios WHERE email = 'carla@ejemplo.com');

-- ---------------------------------------------------------------
-- 2) PEDIDOS
-- Después de cada INSERT, LAST_INSERT_ID() devuelve el id recién
-- creado y lo guardamos en una variable (@p1, @p2, ...).
-- monto_recaudado y estado quedan con sus valores por defecto
-- (0 y 'abierto'); los aportes lo van a ir sumando.
-- ---------------------------------------------------------------
INSERT INTO pedidos (usuario_id, titulo, descripcion, monto_objetivo)
VALUES (@lucia, 'Cirugía para Luna', 'Gata con fractura de cadera que necesita cirugía traumatológica urgente', 120000);
SET @p1 = LAST_INSERT_ID();

INSERT INTO pedidos (usuario_id, titulo, descripcion, monto_objetivo)
VALUES (@martin, 'Alimento para el refugio Patitas', 'Alimento balanceado para 30 perros rescatados durante el próximo mes', 80000);
SET @p2 = LAST_INSERT_ID();

INSERT INTO pedidos (usuario_id, titulo, descripcion, monto_objetivo)
VALUES (@carla, 'Vacunas y castración de gatos callejeros', 'Campaña de vacunación y castración de una colonia de gatos del barrio', 60000);
SET @p3 = LAST_INSERT_ID();

INSERT INTO pedidos (usuario_id, titulo, descripcion, monto_objetivo)
VALUES (@lucia, 'Tratamiento de sarna para Toby', 'Perro rescatado con sarna severa, necesita medicación y baños medicados', 25000);
SET @p4 = LAST_INSERT_ID();

-- El pedido 5 queda SIN aportes a propósito: sirve para ver cómo
-- el reporte con LEFT JOIN muestra pedidos con 0 aportes.
INSERT INTO pedidos (usuario_id, titulo, descripcion, monto_objetivo)
VALUES (@martin, 'Silla de ruedas para Max', 'Perro con parálisis de patas traseras, necesita una silla de ruedas a medida', 90000);
SET @p5 = LAST_INSERT_ID();

-- ---------------------------------------------------------------
-- 3) APORTES
-- Usamos el procedimiento almacenado (no INSERT directo) para que
-- cada aporte actualice monto_recaudado dentro de una transacción.
-- Parámetros: (id del pedido, id del usuario que aporta, monto).
-- ---------------------------------------------------------------
-- Pedido 1 (Luna): 65000 de 120000
CALL sp_registrar_aporte(@p1, @martin, 30000);
CALL sp_registrar_aporte(@p1, @carla,  20000);
CALL sp_registrar_aporte(@p1, @mod,    15000);

-- Pedido 2 (refugio): 80000 de 80000 -> meta lograda, sigue abierto
CALL sp_registrar_aporte(@p2, @lucia, 50000);
CALL sp_registrar_aporte(@p2, @carla, 20000);
CALL sp_registrar_aporte(@p2, @mod,   10000);

-- Pedido 3 (gatos): 20000 de 60000
CALL sp_registrar_aporte(@p3, @lucia,  12000);
CALL sp_registrar_aporte(@p3, @martin,  8000);

-- Pedido 4 (Toby): 25000 de 25000
CALL sp_registrar_aporte(@p4, @martin, 15000);
CALL sp_registrar_aporte(@p4, @carla,  10000);

-- ---------------------------------------------------------------
-- 4) NOVEDADES
-- Las publican los autores de cada pedido. INSERT directo porque
-- no hay procedimiento para novedades.
-- ---------------------------------------------------------------
INSERT INTO novedades (pedido_id, usuario_id, texto) VALUES
(@p1, @lucia,  'Luna ya fue evaluada y la cirugía quedó agendada para la semana próxima.'),
(@p2, @martin, 'Llegó la primera entrega de alimento, gracias a todos los que aportaron.'),
(@p4, @lucia,  'Toby terminó el primer ciclo de baños medicados y ya se le ve mejor.');

-- ---------------------------------------------------------------
-- 5) CIERRE
-- Cerramos el pedido 4 (Toby) con su rendición, igual que lo haría
-- POST /pedidos/{id}/cierre: estado, rendicion y fecha de cierre.
-- ---------------------------------------------------------------
UPDATE pedidos
SET estado = 'cerrado',
    rendicion = 'Se gastaron 18000 pesos en medicación y 7000 en baños medicados. Toby ya está recuperado.',
    cerrado_en = NOW()
WHERE id = @p4;