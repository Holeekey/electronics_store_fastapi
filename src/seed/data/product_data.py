
from src.product.application.commands.create.types.dto import CreateProductDto


product_data: list[CreateProductDto] = [
    CreateProductDto(
        code= "prd12",
        name= "Smartphone NovaTech X50",
        description= "Smartphone de gama alta con triple cámara y pantalla AMOLED",
        cost= 349.99,
        margin= 0.125,
    ),
    CreateProductDto(
        code= "tab87",
        name= "Tablet NovaTech Tab 8 Pro",
        description= "Tablet de 8 pulgadas con gran capacidad de almacenamiento",
        cost= 219.95,
        margin= 0.152,
    ),
    CreateProductDto(
        code= "ear34",
        name= "Auriculares inalámbricos NovaTech AirBuds Pro ",
        description= "Auriculares con cancelación de ruido activa ",
        cost= 119.99,
        margin= 0.108,
    ),
    CreateProductDto(
        code= "wat56",
        name= "Smartwatch NovaTech Fit",
        description= "Smartwatch con GPS integrado y monitor de frecuencia cardíaca",
        cost= 179.5,
        margin= 0.137,
    ),
    CreateProductDto(
        code= "lap98",
        name= "Laptop NovaTech Book Pro",
        description= "Laptop ultradelgada con procesador de última generación",
        cost= 849.99,
        margin= 0.112,
    ),
    CreateProductDto(
        code= "spk21",
        name= "Altavoz inteligente NovaTech Home",
        description= "Altavoz inteligente compatible con asistentes virtuales",
        cost= 89.99,
        margin= 0.141,
    ),
    CreateProductDto(
        code= "cam43",
        name= "Cámara de seguridad NovaTech Eye",
        description= "Cámara de seguridad Wi-Fi con visión nocturna",
        cost= 74.95,
        margin= 0.123,
    ),
    CreateProductDto(
        code= "con65",
        name= "Consola de videojuegos NovaTech Play",
        description= "Consola de videojuegos portátil con juegos preinstalados",
        cost= 249.99,
        margin= 0.155,
    ),
    CreateProductDto(
        code= "drn78",
        name= "Drone NovaTech Sky",
        description= "Drone con cámara 4K y alcance de hasta 2 km",
        cost= 399.99,
        margin= 0.109,
    ),
    CreateProductDto(
        code= "tv90",
        name= "Smart TV NovaTech Vision 55",
        description= "Smart TV de 55 pulgadas con resolución 4K",
        cost= 499.95,
        margin= 0.134,
    ),
    CreateProductDto(
        code= "ear11",
        name= "Auriculares con cable NovaTech Classic",
        description= "Auriculares con cable de alta calidad",
        cost= 34.99,
        margin= 0.116,
    ),
    CreateProductDto(
        code= "bat23",
        name= "Batería externa NovaTech PowerBank",
        description= "Batería externa de alta capacidad",
        cost= 49.95,
        margin= 0.148,
    ),
    CreateProductDto(
        code= "key34",
        name= "Teclado mecánico NovaTech Gamer",
        description= "Teclado mecánico para gaming con retroiluminación RGB",
        cost= 99.99,
        margin= 0.121,
    ),
    CreateProductDto(
        code= "mou56",
        name= "Ratón inalámbrico NovaTech Glide",
        description= "Ratón inalámbrico ergonómico con alta precisión",
        cost= 39.99,
        margin= 0.153
    ),
    CreateProductDto(
        code= "vr78",
        name= "Auriculares VR NovaTech Reality",
        description= "Auriculares de realidad virtual para juegos y experiencias inmersivas",
        cost= 299.99,
        margin= 0.107,
    ),
]