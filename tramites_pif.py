import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8628171494:AAHJAb0luBuFZojCbXKflvtqcki4Y08g5ZY" 

# Diccionario para recordar si el usuario ya recibió el saludo
usuarios_saludados = set()

# Mensaje de saludo personalizado
SALUDO = (
        "👋 *¡Hola!* Soy tu asistente virtual de trámites del\n"
    "Programa de Intervención Familiar. Mi trabajo es explicarte paso a paso y de forma sencilla\n"
    "como realizar tus papeleos."
)



# ========== ESTRUCTURA DE MENÚS ==========

# Menú principal (5 categorías)
menu_principal = [
    [InlineKeyboardButton("🏠 VIVIENDA", callback_data='vivienda')],
    [InlineKeyboardButton("📚 EDUCACIÓN", callback_data='educacion')],
    [InlineKeyboardButton("🏥 SALUD", callback_data='salud')],
    [InlineKeyboardButton("💼 EMPLEO", callback_data='empleo')],
    [InlineKeyboardButton("🤝 AYUDAS SOCIALES", callback_data='ayudas_sociales')],
]

# Submenú de VIVIENDA
submenu_vivienda = [
    [InlineKeyboardButton("Vivienda Protegida", callback_data='vivienda_protegida')],
    [InlineKeyboardButton("Ayudas Alquiler (DAVID)", callback_data='david')],
    [InlineKeyboardButton("Ayudas Alquiler Joven (Emanzipa)", callback_data='emanzipa')],
    [InlineKeyboardButton("Desahucio", callback_data='desahucio')],
    [InlineKeyboardButton("Ayudas Mobiliario", callback_data='mobiliario')],
    [InlineKeyboardButton("Bonos Energéticos", callback_data='bono_energetico')],
    [InlineKeyboardButton("🔙 Volver al menú principal", callback_data='volver')],
]

# Submenú de EDUCACIÓN
submenu_educacion = [
    [InlineKeyboardButton("Escuela Infantil", callback_data='escuela_infantil')],
    [InlineKeyboardButton("Educación Primaria", callback_data='primaria')],
    [InlineKeyboardButton("Educación Secundaria (ESO)", callback_data='eso')],
    [InlineKeyboardButton("Plan Currículo Adaptado (PCA)", callback_data='pca')],
    [InlineKeyboardButton("FP Básica", callback_data='fp_basica')],
    [InlineKeyboardButton("Grado Medio (FP)", callback_data='grado_medio')],
    [InlineKeyboardButton("Grado Superior (FP)", callback_data='grado_superior')],
    [InlineKeyboardButton("Becas y Ayudas", callback_data='becas')],
    [InlineKeyboardButton("Educación Especial (CREENA)", callback_data='necesidades_especiales')],
    [InlineKeyboardButton("🔙 Volver al menú principal", callback_data='volver')],
]

# Submenú de SALUD
submenu_salud = [
    [InlineKeyboardButton("Tarjeta Sanitaria", callback_data='tarjeta_sanitaria')],
    [InlineKeyboardButton("Salud Mental Infantil", callback_data='salud_mental_infantil')],
    [InlineKeyboardButton("Salud Mental Adultos", callback_data='salud_mental_adultos')],
    [InlineKeyboardButton("Centro de Día", callback_data='centro_dia')],
    [InlineKeyboardButton("Unidad Hospitalización (UHP)", callback_data='uhp')],
    [InlineKeyboardButton("Valoración Discapacidad", callback_data='discapacidad')],
    [InlineKeyboardButton("🔙 Volver al menú principal", callback_data='volver')],
]

# Submenú de EMPLEO
submenu_empleo = [
    [InlineKeyboardButton("Prestación Contributiva (PARO)", callback_data='paro')],
    [InlineKeyboardButton("Demanda de Empleo (SNE)", callback_data='demanda_empleo')],
    [InlineKeyboardButton("Equipo EISOL", callback_data='eisol')],
    [InlineKeyboardButton("🔙 Volver al menú principal", callback_data='volver')],
]

# Submenú de AYUDAS SOCIALES
submenu_ayudas = [
    [InlineKeyboardButton("Ingreso Mínimo Vital (IMV)", callback_data='imv')],
    [InlineKeyboardButton("Renta Garantizada", callback_data='renta_garantizada')],
    [InlineKeyboardButton("Ayudas Emergencia Social", callback_data='emergencia_social')],
    [InlineKeyboardButton("Familia Monoparental", callback_data='familia_monoparental')],
    [InlineKeyboardButton("Familia Numerosa", callback_data='familia_numerosa')],
    [InlineKeyboardButton("🔙 Volver al menú principal", callback_data='volver')],
]

# Diccionario para acceder rápidamente a cada submenú
menus = {
    'vivienda': submenu_vivienda,
    'educacion': submenu_educacion,
    'salud': submenu_salud,
    'empleo': submenu_empleo,
    'ayudas_sociales': submenu_ayudas,
}

# ========== TEXTOS INFORMATIVOS (extraídos del documento) ==========

textos_informativos = {
    # ===== VIVIENDA =====
    'vivienda_protegida': (
        "🏠 *VIVIENDA PROTEGIDA*\n\n"
        "Solicitud en la UB de derivación al recurso EISOVI. Servicio del Gobierno de Navarra "
        "gestionado por Fundación Adsis que ofrece orientación sobre posibilidades de alojamiento.\n\n"
        "*REQUISITOS:*\n"
        "• Estar inscrito en el censo de solicitantes de vivienda protegida\n\n"
        "*DOCUMENTACIÓN:*\n"
        "1. DNI/NIE de todos los miembros\n"
        "2. Libro de familia o partidas de nacimiento\n"
        "3. Dos últimas Declaraciones de Renta\n"
        "4. Clave Permanente o Certificado Digital\n"
        "5. Certificado de empadronamiento histórico\n"
        "6. Certificado discapacidad, VG, Familia Numerosa/Monoparental\n"
        "7. Contrato de alquiler o escritura\n"
        "8. Sentencia divorcio o convenio regulador\n"
        "9. Notificación orden desahucio\n"
        "10. Resguardo inscripción censo NASUVINSA\n\n"
        "*ENLACES:*\n"
        "• Censo vivienda protegida: https://www.navarra.es/es/tramites/on/-/line/Censo-de-solicitantes-de-vivienda-protegida\n"
        "• Servicios Sociales Base: https://www.navarra.es/es/derechos-sociales/servicios-sociales-de-base"
    ),
    
    'david': (
        "🏠 *PROGRAMA DAVID - AYUDAS ALQUILER*\n\n"
        "Prestación para el pago de la renta del alquiler a familias con ingresos limitados.\n\n"
        "*REQUISITOS:*\n"
        "• Inscrito en Censo de Vivienda Protegida antes del 31/12 del año anterior\n"
        "• Ingresos mínimos: 3.000€ anuales\n"
        "• Ingresos máximos: 1,7 veces índice SARA\n"
        "• Renta alquiler: no superior a 700€/mes\n\n"
        "*RESTRICCIONES:*\n"
        "• No ser titular de vivienda (o haberla transmitido últimos 5 años)\n"
        "• No tener parentesco con arrendador hasta 2º grado\n"
        "• No haber declarado >5.000€ en ahorros\n"
        "• No ser titular bienes >90.000€\n"
        "• No haber otro beneficiario DAVID en misma vivienda\n\n"
        "*ENLACE:*\n"
        "https://www.nasuvinsa.es/es/servicios/vivienda/david-derecho-subjetivo"
    ),
    
    'emanzipa': (
        "🏠 *EMANZIPA - AYUDAS ALQUILER JOVEN*\n\n"
        "Ayuda económica del 50% de la renta mensual (máx. 280€/mes) para jóvenes.\n\n"
        "*REQUISITOS:*\n"
        "• Edad: 23 a 33 años (a 31 de diciembre)\n"
        "• Ingresos mínimos: 3.000€ anuales\n"
        "• Ingresos máximos: 22.000€ (1 persona) / 33.000€ (2+ personas)\n"
        "• Renta alquiler: no superior a 700€/mes\n\n"
        "*RESTRICCIONES:*\n"
        "• No ser titular de vivienda (últimos 5 años)\n"
        "• No parentesco con arrendador hasta 2º grado\n"
        "• No ahorros >5.000€\n"
        "• No bienes >90.000€\n\n"
        "*ENLACE:*\n"
        "https://www.navarra.es/es/tramites/on/-/line/ayudas-al-alquiler-joven-emanzipa"
    ),
    
    'desahucio': (
        "🏠 *PROTOCOLO DESAHUCIO*\n\n"
        "*PASOS A SEGUIR:*\n\n"
        "1️⃣ *Contactar con Servicios Sociales (Unidad de Barrio)*\n"
        "   • Evaluarán la situación\n"
        "   • Emitirán Informe de Vulnerabilidad (clave para suspensión)\n\n"
        "2️⃣ *Asesoramiento legal (OFIDEL)*\n"
        "   • Servicio gratuito de intermediación hipotecaria\n"
        "   • 📞 Teléfonos: 848 423 376 / 848 421 387 / 848 427 671\n"
        "   • 📧 Email: ofidel@navarra.es\n\n"
        "*DOCUMENTACIÓN PARA VULNERABILIDAD:*\n"
        "• Informe de vulnerabilidad (Servicios Sociales)\n"
        "• Certificado empadronamiento, Libro Familia\n"
        "• Notas simples del Registro de la Propiedad\n"
        "• Declaración responsable ingresos"
    ),
    
    'mobiliario': (
        "🏠 *AYUDAS MOBILIARIO Y ELECTRODOMÉSTICOS*\n\n"
        "Prestación económica puntual para emergencia social.\n\n"
        "*CUANTÍAS:*\n"
        "• 1 persona: hasta 860€/año\n"
        "• 5+ miembros: hasta 1.250€/año\n\n"
        "*PROCEDIMIENTO:*\n"
        "1. Contactar con Unidad de Barrio\n"
        "2. Evaluación por trabajador social\n"
        "3. Presentar presupuesto de tienda\n\n"
        "*CONCEPTOS CUBIERTOS:*\n"
        "Mobiliario básico y electrodomésticos esenciales\n\n"
        "*ENLACE:*\n"
        "https://www.navarra.es/es/derechos-sociales/servicios-sociales-de-base"
    ),
    
    'bono_energetico': (
        "🏠 *BONOS ENERGÉTICOS*\n\n"
        "*BONO SOCIAL ELÉCTRICO:*\n"
        "• Descuento 25% (vulnerable) o 40% (vulnerable severo)\n"
        "• Gestión: con comercializadora de referencia\n"
        "• Info: bonosocial.gob.es\n\n"
        "*BONO SOCIAL TÉRMICO:*\n"
        "• Pago único anual para calefacción, ACS y cocina\n"
        "• Automático para beneficiarios Bono Eléctrico a 31/12\n\n"
        "*TARIFA ÚLTIMO RECURSO (TUR):*\n"
        "• Tarifa de gas regulada por el Gobierno\n\n"
        "*CONTACTO:*\n"
        "Derechos Sociales - C/ González Tablas, 7 - Pamplona\n"
        "📞 848 42 69 00\n"
        "📧 bonosocial@navarra.es\n\n"
        "*ENLACE:*\n"
        "https://www.navarra.es/es/tramites/on/-/line/Certificado-de-circunstancias-especiales-para-la-solicitud-del-bono-social"
    ),
    
    # ===== EDUCACIÓN =====
    'escuela_infantil': (
        "📚 *ESCUELAS INFANTILES MUNICIPALES*\n\n"
        "*FASE 1: PREINSCRIPCIÓN* (marzo-abril)\n"
        "• Telemática: portal Educa (Cl@ve o usuario)\n"
        "• Presencial: cita previa 948 420 098\n"
        "• Centros: Civivox Jus la Rocha\n\n"
        "*DOCUMENTACIÓN:*\n"
        "• DNI/NIE padres\n"
        "• Libro familia o certificado nacimiento\n"
        "• Certificado empadronamiento\n"
        "• Acreditación ingresos, situación laboral\n\n"
        "*FASE 2: MATRÍCULA* (tras listas definitivas)\n"
        "• Presencial en el centro asignado\n"
        "• Verificar documentación original\n\n"
        "*ENLACE:*\n"
        "https://www.pamplona.es/escuelasinfantiles/"
    ),
    
    'primaria': (
        "📚 *EDUCACIÓN PRIMARIA*\n\n"
        "*PROCESO:*\n\n"
        "1️⃣ *Preinscripción* (febrero-marzo)\n"
        "   • Telemática: portal Educa o navarra.es\n"
        "   • Presencial: en el centro elegido\n\n"
        "2️⃣ *Documentación:*\n"
        "   • Impreso solicitud\n"
        "   • Ficha alumno/a\n"
        "   • Libro familia\n"
        "   • Volante empadronamiento\n"
        "   • Certificados (hermanos, discapacidad, renta)\n\n"
        "3️⃣ *Listados:* provisionales (reclamación) y definitivos\n\n"
        "4️⃣ *Matrícula:* presencial en centro asignado (plazo estricto)"
    ),
    
    'eso': (
        "📚 *EDUCACIÓN SECUNDARIA (ESO)*\n\n"
        "*PROCESO DE ADMISIÓN:*\n\n"
        "• Plazo ordinario: marzo-abril\n"
        "• Solicitud telemática: Educa Portal (Cl@ve)\n"
        "• Listados provisionales y definitivos\n"
        "• Matrícula obligatoria en centro asignado\n"
        "• Plazo extraordinario: septiembre\n\n"
        "*CRITERIOS PRIORIDAD:*\n"
        "• Hermanos en centro / proximidad domicilio\n"
        "• Renta per cápita\n"
        "• Discapacidad / víctima VG\n\n"
        "*PARA ADULTOS (ESPA):* Pruebas VIA si no hay certificados\n\n"
        "*ENLACE:*\n"
        "https://www.navarra.es/es/tramites/on/-/line/preinscripcion-y-matricula-del-alumnado-educacion-secundaria-obligatoria-y-bachillerato"
    ),
    
    'pca': (
        "📚 *PLAN CURRÍCULO ADAPTADO (PCA)*\n\n"
        "Programa para alumnado ESO (14-15 años) con dificultades de aprendizaje o conducta.\n\n"
        "*PROCESO:*\n"
        "1. Derivación desde el centro educativo\n"
        "2. Inscripción en listas de oferta (instancia general)\n"
        "3. Asignación de plaza\n"
        "4. Matrícula vía plataforma Educa\n"
        "5. Entrevista de valoración con equipo docente\n\n"
        "*IMPORTANTE:*\n"
        "• Solicitud única por curso\n"
        "• Oferta variable según centro\n"
        "• Entorno flexible e individualizado"
    ),
    
    'fp_basica': (
        "📚 *FP BÁSICA*\n\n"
        "Ciclo formativo de 2 años para jóvenes sin ESO. Obtienes Título Profesional Básico.\n\n"
        "*PROCESO:*\n"
        "1. Inscripción telemática (Secretaría Virtual Educación Navarra)\n"
        "2. Propuesta por consejo orientador\n"
        "3. Publicación listas admitidos\n"
        "4. Formalización matrícula\n\n"
        "*DOCUMENTACIÓN:*\n"
        "• Impreso matrícula firmado\n"
        "• DNI/NIE/Pasaporte alumno y padres\n"
        "• 2 fotos carnet\n"
        "• Email personal\n"
        "• Nº cuenta bancaria\n"
        "• Propuesta final inscripción\n"
        "• Informe síntesis consejo orientador\n\n"
        "*ENLACE:*\n"
        "https://www.navarra.es/es/tramites/on/-/line/inscripcion-en-ciclos-de-grado-basico-de-formacion-profesional"
    ),
    
    'grado_medio': (
        "📚 *GRADO MEDIO (FP)*\n\n"
        "Título de Técnico/a. Modalidad DUAL desde 2024-2025 (prácticas en empresa desde 1º año).\n\n"
        "*PROCESO:*\n"
        "• Preinscripción: abril (ordinario) y septiembre (extraordinario)\n"
        "• Vías: telemática (Secretaría Virtual) o presencial\n"
        "• Listados provisionales y definitivos\n"
        "• Formalización matrícula\n\n"
        "*DOCUMENTACIÓN:*\n"
        "• Impreso matrícula\n"
        "• DNI/NIE/Pasaporte\n"
        "• 2 fotos carnet\n"
        "• Email y datos bancarios\n"
        "• Tasas (aprox. 150€)\n\n"
        "*IMPORTANTE:* Si no entras en 1ª opción, matricúlate en la asignada (lista espera)\n\n"
        "*ENLACE:*\n"
        "https://www.navarra.es/es/tramites/on/-/line/inscripcion-en-ciclos-de-grado-basico-de-formacion-profesional"
    ),
    
    'grado_superior': (
        "📚 *GRADO SUPERIOR (FP)*\n\n"
        "Título de educación superior técnica (2 años). Modalidad DUAL desde 2024-2025.\n\n"
        "*PROCESO:*\n"
        "• Preinscripción: abril y verano\n"
        "• Única solicitud (evitar exclusión)\n"
        "• Listados provisionales y definitivos\n"
        "• Matrícula vía Secretaría Virtual (Cl@ve o DNIe)\n\n"
        "*DOCUMENTACIÓN:*\n"
        "• DNI/NIE/Pasaporte\n"
        "• Título o certificación acceso\n"
        "• 2 fotos carnet\n"
        "• Nº cuenta bancaria\n"
        "• Justificante tasas\n\n"
        "*CONSEJOS:*\n"
        "• Revisar spam para notificaciones\n"
        "• Plazas libres: presencial en centro\n"
        "• No matricularse en más de un centro\n\n"
        "*ENLACE:*\n"
        "https://www.navarra.es/es/tramites/on/-/line/inscripcion-en-ciclos-de-grado-basico-de-formacion-profesional"
    ),
    
    'becas': (
        "📚 *BECAS Y AYUDAS AL ESTUDIO*\n\n"
        "*TIPOS DE AYUDAS:*\n\n"
        "• *Comedor escolar:* para centros públicos y concertados\n"
        "• *Libros de texto:* gratuidad para Primaria y ESO\n"
        "• *Estudios postobligatorios:* Bachillerato, FP y Universidad\n"
        "• *Familias monoparentales:* deducción 600€ en becas postobligatorias\n\n"
        "*ENLACE:*\n"
        "https://www.educacion.navarra.es/web/dpto/becas-y-ayudas"
    ),
    
    'necesidades_especiales': (
        "📚 *RECURSOS EDUCACIÓN ESPECIAL (CREENA)*\n\n"
        "Centro de Recursos para la Educación Especial de Navarra.\n\n"
        "*FUNCIONES:*\n"
        "• Evaluación psicopedagógica\n"
        "• Diseño de apoyos específicos\n"
        "• Formación a familias\n"
        "• Atención Temprana (Escuelas Infantiles)\n\n"
        "*CONTACTO:*\n"
        "📍 C/ Tajonar, 14B, 31006 Pamplona\n"
        "📞 848 431 230\n"
        "📧 creena@educacion.navarra.es\n\n"
        "*ENLACE:*\n"
        "https://creena.educacion.navarra.es/web/"
    ),
    
    # ===== SALUD =====
    'tarjeta_sanitaria': (
        "🏥 *TARJETA SANITARIA (TIS)*\n\n"
        "*OBTENCIÓN:*\n\n"
        "• *Presencial:* Centro de salud (según domicilio)\n"
        "   Documentación: DNI/NIE, volante empadronamiento, documento INSS, libro familia\n\n"
        "• *Online:* navarra.es con Cl@ve o certificado digital\n"
        "• *Tarjeta Virtual:* App Carpeta Personal de Salud\n\n"
        "*CARPETA PERSONAL DE SALUD:*\n"
        "• Consulta informes, resultados, citas, vacunación\n"
        "• Requisito: +16 años y CIPNA\n"
        "• Acceso: Certificado Digital/DNIe o usuario/contraseña (activación online o presencial)"
    ),
    
    'salud_mental_infantil': (
        "🏥 *SALUD MENTAL INFANTO-JUVENIL (CSMIJ)*\n\n"
        "Atención para menores de 0 a 16 años y 11 meses.\n\n"
        "*PROCESO DE DERIVACIÓN:*\n"
        "1. Acudir a Pediatría o Médico de Familia\n"
        "2. Valoración inicial y derivación formal\n"
        "3. Equipo multidisciplinar (psicología y psiquiatría)\n"
        "4. Diagnóstico y plan de tratamiento\n\n"
        "*CENTRO REFERENCIA:*\n"
        "📍 CSMIJ 'Natividad Zubieta' - Avda. Jorge Oteiza, 6, Sarriguren"
    ),
    
    'salud_mental_adultos': (
        "🏥 *SALUD MENTAL ADULTOS*\n\n"
        "*PROCESO DE DERIVACIÓN:*\n"
        "1. Acudir al Médico de Cabecera (atención primaria)\n"
        "2. Evaluación inicial\n"
        "3. Derivación al Centro de Salud Mental (CSM) de referencia\n"
        "4. Equipo multidisciplinar (psiquiatría, psicología, enfermería)\n\n"
        "*CASOS URGENTES:*\n"
        "• Crisis psiquiátrica o riesgo grave\n"
        "• Acudir a urgencias hospitalarias o médico de guardia\n\n"
        "*CENTROS:* Sarriguren, Buztintxuri, Estella, Tudela"
    ),
    
    'centro_dia': (
        "🏥 *CENTRO DE DÍA - DERIVACIÓN*\n\n"
        "*PROCEDIMIENTO:*\n"
        "1. Solicitar cita en Unidad de Barrio o Servicios Sociales Base\n"
        "2. Iniciar trámite reconocimiento dependencia\n"
        "3. Evaluación y resolución del grado\n"
        "4. Elaboración Programa Individual de Atención (PIA)\n"
        "5. Asignación plaza o ayuda económica\n\n"
        "*DOCUMENTACIÓN:*\n"
        "• DNI/NIE solicitante y representante\n"
        "• Tarjeta Sanitaria\n"
        "• Informe médico actualizado\n"
        "• Declaración renta y certificados bancarios\n"
        "• Informe social (elaborado por SS)"
    ),
    
    'uhp': (
        "🏥 *UNIDAD HOSPITALIZACIÓN PSIQUIÁTRICA (UHP)*\n\n"
        "Recurso de atención en crisis. Requiere derivación facultativa exclusiva.\n\n"
        "*PROCESO:*\n"
        "• No puede solicitarse directamente\n"
        "• Indicado por Urgencias, Psiquiatría o Médico Cabecera\n\n"
        "*INGRESO INVOLUNTARIO:*\n"
        "• Notificación al juez en 24h\n"
        "• Ratificación judicial en 72h\n\n"
        "*ACTUACIÓN EN CRISIS:*\n"
        "Contactar inmediatamente con servicios de emergencias"
    ),
    
    'discapacidad': (
        "🏥 *VALORACIÓN DISCAPACIDAD*\n\n"
        "Procedimiento para reconocimiento oficial (≥33%).\n\n"
        "*PROCESO:*\n"
        "1. Acudir a Pediatría o Medicina Familia (informes médicos)\n"
        "2. Solicitud telemática (Navarra.es) o presencial (Unidad Barrio)\n"
        "3. Cita valoración E.V.O. (Equipo Valoración y Orientación)\n"
        "4. Notificación oficial por correo\n\n"
        "*DOCUMENTACIÓN:*\n"
        "• DNI/NIE (o Libro Familia si menor)\n"
        "• Informes sanitarios actualizados\n"
        "• Acreditación tutela/patria potestad\n\n"
        "*CONTACTO:*\n"
        "📍 Cuesta de la Reina, 3, bajo, 31011 Pamplona\n"
        "📞 848 426 900\n"
        "📧 centro.valoracion.discapacidad@navarra.es"
    ),
    
    # ===== EMPLEO =====
    'paro': (
        "💼 *PRESTACIÓN CONTRIBUTIVA (PARO)*\n\n"
        "*REQUISITOS:*\n"
        "• Situación legal de desempleo\n"
        "• Cotizado mínimo 360 días (últimos 6 años)\n"
        "• Inscrito como demandante (SNE-NL)\n"
        "• No haber cumplido edad jubilación\n\n"
        "*PASOS:*\n\n"
        "1️⃣ *Inscribirse como demandante (SNE-NL)*\n"
        "   • Web: https://empleonavarra.es/\n"
        "   • Presencial cita previa (obtener DARDE)\n\n"
        "2️⃣ *Solicitar prestación (SEPE)* - Plazo 15 días hábiles\n"
        "   • Telemática: sede electrónica (Cl@ve/DNIe)\n"
        "   • Presencial: cita previa SEPE\n\n"
        "*CONTACTOS SEPE:*\n"
        "📞 Cita previa: 912 73 83 84\n"
        "📞 Atención: 948 99 00 99 (8-14h)\n"
        "🌐 sepe.gob.es"
    ),
    
    'demanda_empleo': (
        "💼 *TARJETA DEMANDA O MEJORA EMPLEO (SNE)*\n\n"
        "Registro oficial en Servicio Navarro de Empleo (SNE-Nafar Lansare).\n\n"
        "*TIPOS:*\n"
        "• Tarjeta Demanda: desempleo\n"
        "• Tarjeta Mejora: trabajadores que buscan otro empleo\n\n"
        "*CITA PREVIA OBLIGATORIA (1ª inscripción):*\n"
        "📞 848 424 500\n"
        "🌐 https://empleonavarra.es/\n\n"
        "*DOCUMENTACIÓN:*\n"
        "• DNI/NIE/Pasaporte\n"
        "• Currículum Vitae\n"
        "• Títulos académicos originales\n\n"
        "*RENOVACIÓN (SELLAR):* Obligatoria (web, app o cajeros)"
    ),
    
    'eisol': (
        "💼 *EQUIPO INCORPORACIÓN SOCIOLABORAL (EISOL)*\n\n"
        "Servicio del Ayuntamiento de Pamplona para personas con dificultades especiales de acceso al empleo.\n\n"
        "*OBJETIVOS:*\n"
        "• Mejorar empleabilidad (diagnóstico e itinerario a medida)\n"
        "• Inserción real en puestos de trabajo\n\n"
        "*FASES:*\n"
        "1. Acogida e información\n"
        "2. Diagnóstico\n"
        "3. Itinerario personalizado\n"
        "4. Evaluación continua\n\n"
        "*ACCESO:* Derivación de Unidades de Barrio (Servicios Sociales)\n\n"
        "*CONTACTO:*\n"
        "📍 C/ Zapatería 40, 1º, 31001 Pamplona\n"
        "🌐 https://www.pamplona.es/entidades/equipo-de-incorporacion-sociolaboral-eisol"
    ),
    
    # ===== AYUDAS SOCIALES =====
    'imv': (
        "🤝 *INGRESO MÍNIMO VITAL (IMV)*\n\n"
        "Prestación Seguridad Social para personas o unidades de convivencia en vulnerabilidad económica.\n\n"
        "*CANALES TRAMITACIÓN:*\n"
        "• Telemática: sede electrónica (certificado digital, DNIe o Cl@ve)\n"
        "• Presencial: Unidad Administrativa de Tramitación de Navarra\n\n"
        "*CITA PREVIA:* 📞 848 426 900 / 91 541 25 30 / 901 10 65 70\n"
        "*INFORMACIÓN IMV:* 📞 020\n\n"
        "*DOCUMENTACIÓN:*\n"
        "1. Solicitud oficial firmada\n"
        "2. Escrito voluntad (toda unidad)\n"
        "3. DNI/NIE todos integrantes\n"
        "4. Pasaporte y justificante residencia (extranjeros)\n"
        "5. Padrón histórico y colectivo\n"
        "6. Solicitud transferencia (sellada por banco)\n"
        "7. Autorización cobro (si aplica)\n"
        "8. Nóminas o IRPF\n\n"
        "*ENLACES:*\n"
        "• https://sede.seg-social.gob.es/\n"
        "• https://imv.seg-social.es/"
    ),
    
    'renta_garantizada': (
        "🤝 *RENTA GARANTIZADA (RG)*\n\n"
        "Prestación del Gobierno de Navarra para personas/unidades familiares en exclusión social o sin recursos.\n\n"
        "*REQUISITOS:*\n"
        "• Mayor edad o menor emancipado\n"
        "• Residir en Navarra mínimo 2 años (1 año con menores o discapacidad)\n"
        "• Carencia económica acreditada\n\n"
        "*CITA PREVIA OBLIGATORIA:* Unidad de Barrio o Servicio Social Base\n\n"
        "*DOCUMENTACIÓN:*\n"
        "1. Impreso solicitud\n"
        "2. DNI/NIE/Pasaporte de todos\n"
        "3. Libro familia original\n"
        "4. Padrón convivencia (histórico y colectivo)\n"
        "5. Nóminas, IRPF, extractos bancarios\n\n"
        "*DURACIÓN:* 12 meses prorrogables\n"
        "*PLAZO RESOLUCIÓN:* 3 meses\n\n"
        "*CONTACTO:* Servicio Garantía Ingresos - 📞 848 426 900"
    ),
    
    'emergencia_social': (
        "🤝 *AYUDAS EMERGENCIA SOCIAL*\n\n"
        "Gestión local para cubrir gastos básicos (vivienda, alimentación...).\n\n"
        "*PASOS:*\n"
        "1. Cita previa en Unidad de Barrio o Servicio Social Base\n"
        "2. Valoración por trabajador/a social\n\n"
        "*DOCUMENTACIÓN:*\n"
        "• Formulario solicitud firmado\n"
        "• DNI/NIE todos miembros\n"
        "• Libro familia\n"
        "• Certificado empadronamiento y convivencia\n"
        "• Justificantes ingresos últimos 6 meses\n"
        "• Presupuestos o facturas deuda\n\n"
        "*ENLACE:*\n"
        "https://www.navarra.es/es/derechos-sociales/servicios-sociales-de-base"
    ),
    
    'familia_monoparental': (
        "🤝 *FAMILIA MONOPARENTAL - ACREDITACIÓN*\n\n"
        "Certificado oficial con beneficios fiscales y bonificaciones sociales.\n\n"
        "*TIPOS DESTINATARIOS:*\n"
        "• Un progenitor por filiación única, viudedad, patria potestad exclusiva o acogimiento\n"
        "• Custodia exclusiva con ingresos <1,7 SARA, violencia género, progenitor prisión (>1 año), dependencia/invalidez\n\n"
        "*CÓMO SOLICITAR:*\n"
        "• Telemática: navarra.es (certificado digital, DNIe o Cl@ve)\n"
        "• Presencial: Agencia Navarra Autonomía (cita 848 425046), SS Base, Unidades Barrio, trabajadores sociales centros salud\n\n"
        "*DOCUMENTACIÓN:*\n"
        "1. Formulario solicitud\n"
        "2. Padrón convivencia (<2 meses)\n"
        "3. Libro familia completo\n"
        "4. DNI/NIE todos miembros\n"
        "5. Declaración IRPF (o certificados subsidios/RG)\n"
        "6. Matrícula estudios (hijos 21+)\n"
        "7. Declaración ingresos hijos <IPREM\n"
        "8. Sentencias custodia, órdenes protección o informes invalidez\n\n"
        "*ENLACE:*\n"
        "https://www.navarra.es/es/tramites/on/-/line/acreditacion-de-familia-monoparental"
    ),
    
    'familia_numerosa': (
        "🤝 *FAMILIA NUMEROSA - ACREDITACIÓN*\n\n"
        "Certificado con beneficios fiscales y bonificaciones sociales.\n\n"
        "*CATEGORÍA GENERAL:*\n"
        "• 1-2 ascendientes con 3+ hijos (<21 años o <25 con estudios)\n"
        "• 2 hijos si uno o progenitor tiene discapacidad ≥33%\n\n"
        "*CÓMO SOLICITAR:*\n"
        "• Telemática: sede electrónica Navarra (certificado digital, DNIe o Cl@ve)\n"
        "• Presencial: Agencia Navarra Autonomía (cita 848 425046), SS Base, Unidades Barrio, trabajadores sociales centros salud\n\n"
        "*DOCUMENTACIÓN:*\n"
        "1. Formulario solicitud firmado\n"
        "2. Certificado empadronamiento actual\n"
        "3. Libro familia completo\n"
        "4. DNI padres e hijos (≥14 años)\n"
        "5. Declaración IRPF (para categoría especial renta)\n"
        "6. Matrícula estudios (hijos 21-25 años)\n"
        "7. Justificantes ingresos hijos <IPREM\n"
        "8. Resolución discapacidad (si aplica)\n\n"
        "*ENLACE:*\n"
        "https://www.navarra.es/es/tramites/on/-/line/Acreditacion-de-familia-numerosa"
    ),
}

# ========== FUNCIONES DEL BOT ==========

async def mostrar_menu_principal(mensaje):
    """Envía el menú principal con los 5 botones"""
    await mensaje.reply_text(
        "🏠 *Menú principal de trámites*\n\nElige una categoría para comenzar:",
        reply_markup=InlineKeyboardMarkup(menu_principal),
        parse_mode="Markdown"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Saludo personalizado (solo la primera vez)
    if user_id not in usuarios_saludados:
        await update.message.reply_text(SALUDO)
        usuarios_saludados.add(user_id)
        await asyncio.sleep(1)
    
    # Mostrar menú principal
    await mostrar_menu_principal(update.message)

async def cualquier_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in usuarios_saludados:
        await update.message.reply_text(SALUDO)
        usuarios_saludados.add(user_id)
        await asyncio.sleep(1)
    
    await mostrar_menu_principal(update.message)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    # Si es una categoría principal (vivienda, educacion, etc.) -> mostrar su submenú
    if data in menus:
        titulos = {
            'vivienda': '🏠 VIVIENDA',
            'educacion': '📚 EDUCACIÓN',
            'salud': '🏥 SALUD',
            'empleo': '💼 EMPLEO',
            'ayudas_sociales': '🤝 AYUDAS SOCIALES'
        }
        await query.edit_message_text(
            text=f"📂 *{titulos.get(data, data.upper())}* - ¿Qué trámite necesitas?",
            reply_markup=InlineKeyboardMarkup(menus[data]),
            parse_mode="Markdown"
        )
    # Si es una opción final (tiene texto informativo)
    elif data in textos_informativos:
        # Mostrar la información del trámite
        await query.edit_message_text(
            text=textos_informativos[data],
            parse_mode="Markdown"
        )
        # Esperar 3 segundos y volver al menú principal
        await asyncio.sleep(3)
        await query.message.reply_text(
            "🏠 *Volvemos al menú principal*",
            reply_markup=InlineKeyboardMarkup(menu_principal),
            parse_mode="Markdown"
        )
    # Botón de volver
    elif data == 'volver':
        await query.edit_message_text(
            text="🏠 *Menú principal*",
            reply_markup=InlineKeyboardMarkup(menu_principal),
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text("❌ Opción no válida. Por favor, usa los botones.")

# ========== ARRANQUE DEL BOT ==========

def main():
    # Para Python 3.14+
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    
    if loop and loop.is_running():
        # Si ya hay un loop corriendo, creamos una tarea
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cualquier_texto))
        app.add_handler(CallbackQueryHandler(callback_handler))
        
        async def run():
            await app.initialize()
            await app.updater.start_polling()
            await app.idle()
        
        asyncio.create_task(run())
    else:
        # Método tradicional
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cualquier_texto))
        app.add_handler(CallbackQueryHandler(callback_handler))
        app.run_polling()
