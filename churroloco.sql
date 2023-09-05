-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-09-2023 a las 17:10:25
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `churroloco`
--
CREATE DATABASE IF NOT EXISTS `churroloco` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `churroloco`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `informes`
--

CREATE TABLE `informes` (
  `id_informes` int(255) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `nombre` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `informes`
--

INSERT INTO `informes` (`id_informes`, `fecha`, `nombre`) VALUES
(6, '2023-07-11 17:18:15.000000', '2023-07-11__17_18_15_Informe_Ventas.xls'),
(7, '2023-07-11 17:23:22.000000', '2023-07-11__17_23_22_Informe_Ventas.xls'),
(9, '2023-07-21 15:59:07.000000', '2023-07-21__15_59_07_Informe_Ventas.xls'),
(10, '2023-07-21 15:59:15.000000', '2023-07-21__15_59_15_Informe_Ventas.xls');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido`
--

CREATE TABLE `pedido` (
  `id_pedido` int(255) NOT NULL,
  `fecha` varchar(255) NOT NULL,
  `id_producto_pedido` int(255) NOT NULL,
  `id_usuario_pedido` int(255) NOT NULL,
  `cantidad_pedido` int(255) NOT NULL,
  `estado` varchar(255) NOT NULL,
  `nombre_numero_servicios_pedido` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedido`
--

INSERT INTO `pedido` (`id_pedido`, `fecha`, `id_producto_pedido`, `id_usuario_pedido`, `cantidad_pedido`, `estado`, `nombre_numero_servicios_pedido`) VALUES
(130, '01/10/2023 22:38:00', 118, 10, 1, 'Pago', 'mesa_58'),
(131, '01/09/2023 22:38:00', 119, 10, 1, 'Pago', 'mesa_58'),
(132, '01/09/2023 22:38:00', 120, 10, 1, 'Pago', 'mesa_58'),
(133, '01/09/2023 22:38:00', 121, 10, 1, 'Pago', 'mesa_58'),
(134, '01/10/2023 22:38:48', 118, 10, 5, 'Pago', 'mesa_2'),
(135, '01/09/2023 22:38:56', 118, 10, 4, 'Pago', 'mesa_98'),
(136, '01/09/2023 22:58:18', 121, 10, 1, 'Pago', 'domicilio_20'),
(137, '02/09/2023 00:27:09', 119, 10, 1, 'Pago', 'mesa_2'),
(138, '02/09/2023 09:00:49', 120, 10, 1, 'Pago', 'mesa_2'),
(139, '02/09/2023 09:00:49', 121, 10, 1, 'Pago', 'mesa_2'),
(140, '02/09/2023 09:00:49', 122, 10, 1, 'Pago', 'mesa_2'),
(141, '02/09/2023 09:09:37', 118, 29, 1, 'Pago', 'mesa_3'),
(142, '02/09/2023 09:09:37', 119, 29, 1, 'Pago', 'mesa_3'),
(143, '02/09/2023 09:09:37', 120, 29, 1, 'Pago', 'mesa_3'),
(144, '02/09/2023 09:09:37', 121, 29, 1, 'Pago', 'mesa_3'),
(145, '02/09/2023 09:09:37', 122, 29, 1, 'Pago', 'mesa_3'),
(147, '02/09/2023 09:26:50', 125, 10, 2, 'Pago', 'mesa_2'),
(148, '02/09/2023 09:26:50', 121, 10, 1, 'Pago', 'mesa_2'),
(149, '', 120, 10, 1, 'Seleccionado', 'mesa_3'),
(150, '', 121, 10, 1, 'Seleccionado', 'mesa_3'),
(151, '02/09/2023 09:52:06', 119, 10, 1, 'Pago', 'mesa_58'),
(152, '', 121, 10, 1, 'Seleccionado', 'mesa_58'),
(153, '', 120, 10, 1, 'Seleccionado', 'domicilio_3'),
(154, '', 122, 10, 1, 'Seleccionado', 'domicilio_20');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL,
  `nombre_producto` varchar(255) NOT NULL,
  `descripcion_producto` varchar(255) NOT NULL,
  `imagen_producto` varchar(255) NOT NULL,
  `precio_producto` decimal(65,0) NOT NULL,
  `cantidad_existente_producto` int(255) NOT NULL,
  `tipo_producto` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `nombre_producto`, `descripcion_producto`, `imagen_producto`, `precio_producto`, `cantidad_existente_producto`, `tipo_producto`) VALUES
(118, 'Brisa', '350Ml', 'agua.png', 1200, 9, 1),
(119, 'Cristal', '350Ml', 'agua2.png', 1700, 8, 1),
(120, 'Aguila', '1L', 'cerveza.png', 10500, 97, 3),
(121, 'Corona', 'Caja 12', 'cerveza2.png', 21700, 5, 7),
(122, 'Cocacola', '350 Ml', '2023175622_1535.jpg', 1300, 7, 8),
(125, 'A4', '350 Ml', '2023092457_supermercados_la_vaquita_supervaquita_gaseosa_quatro_400ml_bebidas_liquidas_1024x1024.webp', 5000, 0, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `id_servicios` int(11) NOT NULL,
  `numero_servicio` int(255) NOT NULL,
  `nombre_servicio` varchar(255) NOT NULL,
  `estado_servicio` varchar(255) NOT NULL,
  `descripcion_servicio` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicios`
--

INSERT INTO `servicios` (`id_servicios`, `numero_servicio`, `nombre_servicio`, `estado_servicio`, `descripcion_servicio`) VALUES
(127, 19, 'domicilio', 'Disponible', ''),
(128, 20, 'domicilio', 'Ocupado', ''),
(130, 58, 'mesa', 'Ocupado', ''),
(131, 98, 'mesa', 'Disponible', ''),
(135, 2, 'domicilio', 'Disponible', ''),
(137, 3, 'domicilio', 'Ocupado', ''),
(139, 2, 'mesa', 'Disponible', ''),
(141, 1, 'domicilio', 'Disponible', ''),
(142, 3, 'mesa', 'Ocupado', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `temp_img`
--

CREATE TABLE `temp_img` (
  `nombre_temp` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_producto`
--

CREATE TABLE `tipo_producto` (
  `id_tipo_producto` int(100) NOT NULL,
  `nombre_tipo_producto` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipo_producto`
--

INSERT INTO `tipo_producto` (`id_tipo_producto`, `nombre_tipo_producto`) VALUES
(1, 'Aguas Y Gaseosas'),
(3, 'Cervezas'),
(7, 'Aves'),
(8, 'Licor'),
(9, 'Vinos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int(255) NOT NULL,
  `nombre_usuario` varchar(255) NOT NULL,
  `apellido_usuario` varchar(255) NOT NULL,
  `imagen_usuario` varchar(255) NOT NULL,
  `usuario_usuario` varchar(255) NOT NULL,
  `contraseña_usuario` varchar(255) NOT NULL,
  `tipo_usuario` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `nombre_usuario`, `apellido_usuario`, `imagen_usuario`, `usuario_usuario`, `contraseña_usuario`, `tipo_usuario`) VALUES
(10, 'brayan', 'brayan', '2023075551_Wolf.jpg', 'admin', '123', 'Administrador'),
(26, 'Usuario2', 'Apellido', '2023074714_lindo-unicornio-bebiendo-te-leche-boba-ilustracion-icono-vector-dibujos-animados-arco-iris-icono-beb.jpg', 'emple2', '123', 'Empleado'),
(29, 'Usuario1', 'Apellido', '2023074804_poster504x498f8f8f8-pad600x600f8f8f8.jpg', 'empl', '123', 'Empleado'),
(32, 'pepe', 'elgrillo', '2023090742_cerveza.png', 'sup', '123', 'Administrador');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `informes`
--
ALTER TABLE `informes`
  ADD PRIMARY KEY (`id_informes`);

--
-- Indices de la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD PRIMARY KEY (`id_pedido`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`) USING BTREE;

--
-- Indices de la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD PRIMARY KEY (`id_servicios`) USING BTREE;

--
-- Indices de la tabla `tipo_producto`
--
ALTER TABLE `tipo_producto`
  ADD PRIMARY KEY (`id_tipo_producto`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `informes`
--
ALTER TABLE `informes`
  MODIFY `id_informes` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `pedido`
--
ALTER TABLE `pedido`
  MODIFY `id_pedido` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=155;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=126;

--
-- AUTO_INCREMENT de la tabla `servicios`
--
ALTER TABLE `servicios`
  MODIFY `id_servicios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=143;

--
-- AUTO_INCREMENT de la tabla `tipo_producto`
--
ALTER TABLE `tipo_producto`
  MODIFY `id_tipo_producto` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
