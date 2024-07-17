from core.database import engine
from models.breach import Breach
from models.data_leak import DataLeak
from models.data_type import DataType
from models.security_tip import SecurityTip
from sqlalchemy.orm import Session
from utils.crytpography import get_hash

# from models.password import Password


def populate_dummy_data():
    session = Session(bind=engine)
    data_type = session.query(DataType).first()
    if data_type is not None:
        session.close()
        return

    # Initial DataTypes
    data_types: dict[str, DataType] = {
        "email": DataType(id=1, name="email", display_name="Correo electrónico"),
        "rut": DataType(id=2, name="rut", display_name="RUT"),
        "phone": DataType(id=3, name="phone", display_name="Número telefónico"),
        "credit_card": DataType(
            id=4, name="credit_card", display_name="Tarjeta de crédito"
        ),
        "address": DataType(id=5, name="address", display_name="Domicilio"),
        "ip_address": DataType(id=6, name="ip_address", display_name="Dirección IP"),
        "name": DataType(id=7, name="name", display_name="Nombre"),
        "password": DataType(id=8, name="password", display_name="Contraseña"),
        "purchase_records": DataType(
            id=9, name="purchase_records", display_name="Registro de compras"
        ),
        "passport": DataType(id=10, name="passport", display_name="Número pasaporte"),
        "birthdate": DataType(
            id=11, name="birthdate", display_name="Fecha de nacimiento"
        ),
        "username": DataType(id=12, name="username", display_name="Nombre de usuario"),
        "download_records": DataType(
            id=13, name="download_records", display_name="Historial de descargas"
        ),
        "gender": DataType(id=14, name="gender", display_name="Género"),
        "locations": DataType(
            id=15, name="locations", display_name="Ubicaciones de uso"
        ),
        "private_msgs": DataType(
            id=16, name="private_msgs", display_name="Mensajes privados"
        ),
        "profile_picture": DataType(
            id=17, name="profile_picture", display_name="Foto de perfil"
        ),
    }
    session.add_all(list(data_types.values()))
    session.commit()

    # Breaches
    breaches: list[Breach] = [
        Breach(
            id=1,
            name="Entel",
            description="El año 2022, Entel fue víctima de un hackeo masivo que afectó a más de 250.000 clientes. Filtrándose mucha información sensible de estos.",
            breach_date="2022-07-26",
            confirmed=True,
            is_sensitive=False,
            data_breached=[
                data_types["phone"],
                data_types["rut"],
                data_types["address"],
                data_types["name"],
            ],
        ),
        Breach(
            id=2,
            name="Banco Estado",
            description="El año 2023, BancoEstado sufrió una filtración de su base de datos, que comprometió alrededor de 52.000 clientes.",
            breach_date="2023-11-08",
            confirmed=True,
            is_sensitive=False,
            data_breached=[
                data_types["email"],
                data_types["password"],
                data_types["rut"],
                data_types["name"],
                data_types["credit_card"],
            ],
        ),
        Breach(
            id=3,
            name="Ripley",
            description="En el año 2022, Ripley publicó involuntariamente informacion de compras de 9.000 usuarios.",
            breach_date="2022-08-18",
            confirmed=True,
            is_sensitive=False,
            data_breached=[
                data_types["email"],
                data_types["name"],
                data_types["address"],
                data_types["ip_address"],
            ],
        ),
        Breach(
            id=4,
            name="Jumbo",
            description="La importante cadena de supermercados Jumbo anunció el descubrimiento de una filtración de datos que comprometió la información personal de sus clientes. La brecha de seguridad, detectada e junio del año 2018, expuso nombres, direcciones de correo electrónico, números de teléfono y registros de compras de millones de clientes.",
            breach_date="2018-06-29",
            confirmed=True,
            is_sensitive=False,
            data_breached=[
                data_types["email"],
                data_types["name"],
                data_types["phone"],
                data_types["purchase_records"],
            ],
        ),
        Breach(
            id=5,
            name="LATAM",
            description="La aerolínea LATAM anunció el descubrimiento de una filtración de datos que afectó a su sistema de reservas. La brecha de seguridad, detectada en julio del año 2019, expuso información personal y detalles de viaje de miles de pasajeros que volaron en la aerolínea en las fechas entre marzo y julio del 2019. Los datos comprometidos incluyen nombres, números de pasaporte, RUT, números de tarjetas de crédito asociadas a reservas, detalles de itinerario y preferencias de viaje.",
            breach_date="2019-07-19",
            confirmed=True,
            is_sensitive=False,
            data_breached=[
                data_types["name"],
                data_types["passport"],
                data_types["rut"],
                data_types["credit_card"],
                data_types["purchase_records"],
            ],
        ),
        Breach(
            id=6,
            name="Farmacias Cruz Verde",
            description="La cadena de farmacias Cruz Verde anunció el descubrimiento de una filtración de datos que afectó a su sistema de gestión de clientes. Esta filtración de datos, identificada el 02 de octubre del año 2019, comprometió información sensible de clientes que utilizaron servicios como recetas médicas y programas de fidelidad entre mayo y agosto de 2019. Los datos filtrados incluyen nombres, fechas de nacimiento, direcciones, RUT, historiales de medicación y detalles de compras de medicamentos.",
            breach_date="2019-10-02",
            confirmed=True,
            is_sensitive=False,
            data_breached=[
                data_types["name"],
                data_types["rut"],
                data_types["address"],
                data_types["purchase_records"],
                data_types["birthdate"],
            ],
        ),
        Breach(
            id=7,
            name="Falabella",
            description="La conocida cadena de tiendas de retail, Falabella, anunció una filtración de datos que afectó a su sistema de ventas en línea. La brecha de seguridad, detectada en julio del año 2022, comprometió la información personal y financiera de clientes que realizaron compras en línea entre marzo y julio de ese mismo año. Los datos filtrados incluyen nombres, direcciones de envío, números de tarjetas de crédito, fechas de vencimiento y códigos de seguridad.",
            breach_date="2022-07-29",
            confirmed=True,
            is_sensitive=False,
            data_breached=[
                data_types["email"],
                data_types["name"],
                data_types["address"],
                data_types["credit_card"],
            ],
        ),
        Breach(
            id=8,
            name="VTR",
            description="El proveedor de servicios de internet, VTR, anunció el descubrimiento de una filtración de datos que afectó a su sistema de gestión de clientes. La brecha de seguridad, identificada el 4 de septiembre del año 2023, comprometió información confidencial de sus suscriptores que utilizaron los servicios de internet entre junio y septiembre de ese mismo año. Los datos filtrados incluyen nombres de usuario, direcciones de correo electrónico, direcciones IP asignadas, detalles de facturación y registros de actividad en línea.",
            breach_date="2023-09-04",
            confirmed=True,
            is_sensitive=False,
            data_breached=[
                data_types["rut"],
                data_types["email"],
                data_types["username"],
                data_types["password"],
                data_types["ip_address"],
            ],
        ),
        Breach(
            id=9,
            name="The Pirate Bay",
            description="The Pirate Bay, el famoso sitio web de intercambio de archivos, anunció una grave filtración de datos que afectó a su base de usuarios. La brecha de seguridad, descubierta el 3 de julio de 2021, comprometió la información de millones de usuarios registrados entre enero y junio de ese mismo año. Los datos filtrados incluyen nombres de usuario, direcciones de correo electrónico, contraseñas cifradas, direcciones IP y detalles de las descargas realizadas.",
            breach_date="2021-07-03",
            confirmed=True,
            is_sensitive=True,
            data_breached=[
                data_types["username"],
                data_types["email"],
                data_types["password"],
                data_types["ip_address"],
                data_types["download_records"],
            ],
        ),
        Breach(
            id=10,
            name="Tinder",
            description="La popular aplicación de citas Tinder anunció el descubrimiento de una filtración de datos que afectó a su base de usuarios. La brecha de seguridad, detectada el 8 de marzo del 2024, comprometió la información personal de millones de usuarios que utilizaron la plataforma entre noviembre de 2023 y febrero de 2024. Los datos filtrados incluyen nombres, edades, número móvil, ubicaciones, géneros, mensajes privados y fotos de perfil.",
            breach_date="2024-03-10",
            confirmed=True,
            is_sensitive=True,
            data_breached=[
                data_types["phone"],
                # data_types["email"],
                data_types["name"],
                data_types["birthdate"],
                data_types["locations"],
                data_types["gender"],
                data_types["private_msgs"],
                data_types["profile_picture"],
            ],
        ),
    ]
    session.add_all(breaches)
    session.commit()
    # session.refresh(breaches)

    # DataLeaks
    data_leaks = [
        DataLeak(
            id=1,
            hash_value=get_hash("nico@example.com"),
            data_type=data_types["email"],
            breach_id=2,
            found_with=[
                data_types["credit_card"],
                data_types["rut"],
                data_types["name"],
            ],
        ),
        DataLeak(
            id=2,
            hash_value=get_hash("nico@example.com"),
            data_type=data_types["email"],
            breach_id=3,
            found_with=[
                data_types["address"],
                data_types["name"],
            ],
        ),
        DataLeak(
            id=3,
            hash_value=get_hash("911111111"),
            data_type=data_types["phone"],
            breach_id=1,
            found_with=[
                data_types["rut"],
                data_types["address"],
                data_types["name"],
            ],
        ),
        DataLeak(
            id=4,
            hash_value=get_hash("111111111"),
            data_type=data_types["rut"],
            breach_id=1,
            found_with=[
                data_types["email"],
                data_types["address"],
                data_types["name"],
            ],
        ),
        DataLeak(
            id=5,
            hash_value=get_hash("111111111"),
            data_type=data_types["rut"],
            breach_id=3,
            found_with=[
                data_types["email"],
                data_types["ip_address"],
                data_types["name"],
            ],
        ),
        DataLeak(
            id=6,
            hash_value=get_hash("nico@example.com"),
            data_type=data_types["email"],
            breach_id=2,
            found_with=[
                data_types["credit_card"],
                data_types["rut"],
                data_types["name"],
            ],
        ),
        DataLeak(
            id=7,
            hash_value=get_hash("nico@example.com"),
            data_type=data_types["email"],
            breach_id=9,
            found_with=[
                data_types["password"],
                data_types["ip_address"],
                data_types["download_records"],
            ],
        ),
        DataLeak(
            id=8,
            hash_value=get_hash("+56912345678"),
            data_type=data_types["phone"],
            # hash_value=get_hash("nico@example.com"),
            # data_type=data_types["email"],
            breach_id=10,
            found_with=[
                data_types["name"],
                data_types["birthdate"],
                data_types["locations"],
                data_types["private_msgs"],
                data_types["profile_picture"],
            ],
        ),
    ]
    session.add_all(data_leaks)
    session.commit()

    # Security Tips
    security_tips: list[SecurityTip] = [
        SecurityTip(
            data_type_id=data_types["email"].id,
            description="Manténgase atenta(o) a posibles correos electrónicos fraudulentos.",
        ),
        SecurityTip(
            data_type_id=data_types["phone"].id,
            description="Manténgase atenta(o) a posibles llamadas o mensajes de textos fraudulentos.",
        ),
        SecurityTip(
            data_type_id=data_types["password"].id,
            description="Cambie esta contraseña en todas las cuentas que la utilicen, y no vuelva a utilizar esta misma contraseña nuevamente.",
        ),
        SecurityTip(
            data_type_id=data_types["credit_card"].id,
            description="Bloquee su tarjeta de crédito y/o avise al banco que es posible que su tarjeta haya sido comprometida por terceros.",
        ),
    ]
    session.add_all(security_tips)
    session.commit()

    # Se cierra conexión
    session.close()
