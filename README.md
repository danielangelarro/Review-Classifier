# Review-Classifier

## Authors

- Daniel Ángel Arró Moreno
- Pedro Pablo Álvarez Portelles
- Abel Llerena Domingo


## Problema

El contenido de las reseñas generado por un usuario es útil para que los compradores tomen decisiones
más informadas en sitios web de compras en lı́nea. Sin embargo, debido al gran volumen de reseñas,
especialmente de artı́culos populares, es muy difı́cil para cualquiera encontrar fácilmente información
relevante. A menudo, el sitio web sólo proporciona algunos métodos de clasificación simples, pero no
muy útiles, como clasificación por tiempo o calificación por votos de utilidad. Se pueden considerar va-
rios factores para este propósito, incluido el historial de compras reciente del usuario y el de navegación
y las propiedades de los artı́culos.

Se propone un sistema que haga uso de lo antes mencionado, junto a otras caracterı́sticas que se consideran
necesarias, para que los compradores sugieran mejores compras a los usuarios.


## Requirements


## APIs


## Installation

### Construir la imagen y correr el proyecto

1. **Construir y levantar los servicios**:

    ```bash
    ./script.sh build
    ./script.sh up
    ```

2. **Crear las migraciones y actualizar la base de datos**:

    ```bash
    ./script.sh create_migration "Add user and user history tables"
    ./script.sh migrate
    ```

3. **Ejecutar las pruebas**:

    ```bash
    ./script.sh test
    ```

4. **Detener los servicios**:

    ```bash
    ./script.sh down
    ```

5. **Uso local sin Docker**:

    Asegúrate de tener PostgreSQL instalado y configurado localmente con las credenciales adecuadas.

    - **Migrar localmente**:

        ```bash
        ./script.sh local_migrate
        ```

    - **Correr pruebas localmente**:

        ```bash
        ./script.sh local_test
        ```
